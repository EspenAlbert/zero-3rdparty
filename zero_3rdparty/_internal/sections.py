from __future__ import annotations

import logging
import re
from dataclasses import dataclass, field
from enum import StrEnum
from pathlib import Path

logger = logging.getLogger(__name__)


def slug(text: str) -> str:
    """Convert text to lowercase slug suitable for section marker IDs."""
    s = re.sub(r"[^\w\s-]", "", text.lower())
    return re.sub(r"[-\s]+", "_", s).strip("_")


@dataclass(frozen=True)
class CommentConfig:
    prefix: str
    suffix: str = ""


@dataclass
class SectionPart:
    content: str
    start_line: int
    end_line: int
    content_after: str | None = None


@dataclass
class Section:
    id: str
    parts: list[SectionPart] = field(default_factory=list)
    content_after: str | None = None

    @property
    def content(self) -> str:
        return "\n".join(p.content for p in self.parts)

    @property
    def start_line(self) -> int:
        return self.parts[0].start_line if self.parts else -1

    @property
    def end_line(self) -> int:
        return self.parts[-1].end_line if self.parts else -1


@dataclass
class SectionChanges:
    modified: list[str]
    missing: list[str]


class _ParseState(StrEnum):
    OUTSIDE = "outside"
    IN_SECTION = "in_section"
    PAUSED = "paused"


EXTENSION_COMMENT_MAP: dict[str, CommentConfig] = {
    # Hash comments
    ".py": CommentConfig("#"),
    ".yaml": CommentConfig("#"),
    ".yml": CommentConfig("#"),
    ".toml": CommentConfig("#"),
    ".sh": CommentConfig("#"),
    ".bash": CommentConfig("#"),
    ".zsh": CommentConfig("#"),
    ".r": CommentConfig("#"),
    ".R": CommentConfig("#"),
    # HTML-style comments
    ".md": CommentConfig("<!--", " -->"),
    ".mdc": CommentConfig("<!--", " -->"),
    ".html": CommentConfig("<!--", " -->"),
    ".xml": CommentConfig("<!--", " -->"),
    ".svg": CommentConfig("<!--", " -->"),
    # C-style line comments
    ".js": CommentConfig("//"),
    ".ts": CommentConfig("//"),
    ".jsx": CommentConfig("//"),
    ".tsx": CommentConfig("//"),
    ".go": CommentConfig("//"),
    ".c": CommentConfig("//"),
    ".cpp": CommentConfig("//"),
    ".h": CommentConfig("//"),
    ".java": CommentConfig("//"),
    ".kt": CommentConfig("//"),
    ".swift": CommentConfig("//"),
    ".rs": CommentConfig("//"),
    ".scala": CommentConfig("//"),
    ".groovy": CommentConfig("//"),
    # C-style block comments (single line)
    ".css": CommentConfig("/*", " */"),
    ".scss": CommentConfig("/*", " */"),
    ".less": CommentConfig("/*", " */"),
    # SQL
    ".sql": CommentConfig("--"),
    # Lua
    ".lua": CommentConfig("--"),
}

FILENAME_COMMENT_MAP: dict[str, CommentConfig] = {
    "justfile": CommentConfig("#"),
    "Makefile": CommentConfig("#"),
    "Dockerfile": CommentConfig("#"),
    ".gitignore": CommentConfig("#"),
    ".dockerignore": CommentConfig("#"),
    ".env": CommentConfig("#"),
    ".editorconfig": CommentConfig("#"),
    "uv.lock": CommentConfig("#"),
    "CODEOWNERS": CommentConfig("#"),
    "LICENSE": CommentConfig("#"),
}


def get_comment_config(path: Path | str, override: CommentConfig | None = None) -> CommentConfig:
    if override:
        return override
    p = Path(path) if isinstance(path, str) else path
    if config := EXTENSION_COMMENT_MAP.get(p.suffix):
        return config
    if config := FILENAME_COMMENT_MAP.get(p.name):
        return config
    raise ValueError(f"No comment config for: {p.name} (extension={p.suffix!r})")


def _build_start_pattern(tool_name: str, config: CommentConfig) -> re.Pattern[str]:
    return re.compile(
        rf"^\s*{re.escape(config.prefix)}\s*===\s*DO_NOT_EDIT:\s*"
        rf"{re.escape(tool_name)}\s+(?P<id>[\w-]+)\s*==={re.escape(config.suffix)}$",
        re.MULTILINE,
    )


def _build_end_pattern(tool_name: str, config: CommentConfig) -> re.Pattern[str]:
    return re.compile(
        rf"^\s*{re.escape(config.prefix)}\s*===\s*OK_EDIT:\s*"
        rf"{re.escape(tool_name)}\s+(?P<end_id>[\w-]+)\s*==={re.escape(config.suffix)}$",
        re.MULTILINE,
    )


def _start_marker(tool_name: str, section_id: str, config: CommentConfig) -> str:
    return f"{config.prefix} === DO_NOT_EDIT: {tool_name} {section_id} ==={config.suffix}"


def _end_marker(tool_name: str, section_id: str, config: CommentConfig) -> str:
    return f"{config.prefix} === OK_EDIT: {tool_name} {section_id} ==={config.suffix}"


def parse_sections(  # noqa: C901
    content: str,
    tool_name: str,
    config: CommentConfig,
    filename: str = "",
) -> list[Section]:
    start_pattern = _build_start_pattern(tool_name, config)
    end_pattern = _build_end_pattern(tool_name, config)
    lines = content.split("\n")
    sections_by_id: dict[str, Section] = {}
    section_order: list[str] = []
    file_suffix = f" in {filename}" if filename else ""

    state = _ParseState.OUTSIDE
    current_id: str = ""
    current_start: int = -1
    content_lines: list[str] = []
    after_lines: list[str] = []

    for i, line in enumerate(lines):
        start_match = start_pattern.match(line)
        end_match = end_pattern.match(line)

        if state == _ParseState.OUTSIDE:
            if start_match:
                current_id = start_match.group("id")
                current_start = i
                content_lines = []
                sections_by_id.setdefault(current_id, Section(id=current_id, parts=[]))
                if current_id not in section_order:
                    section_order.append(current_id)
                state = _ParseState.IN_SECTION
        elif state == _ParseState.IN_SECTION:
            if end_match:
                end_id = end_match.group("end_id")
                if end_id != current_id:
                    raise ValueError(
                        f"Mismatched section end at line {i}: expected '{current_id}', got '{end_id}'{file_suffix}"
                    )
                sections_by_id[current_id].parts.append(SectionPart("\n".join(content_lines), current_start, i))
                after_lines = []
                state = _ParseState.PAUSED
            elif start_match:
                raise ValueError(
                    f"Nested section at line {i}: found '{start_match.group('id')}' inside '{current_id}'{file_suffix}"
                )
            else:
                content_lines.append(line)
        elif state == _ParseState.PAUSED:
            if start_match:
                match_id = start_match.group("id")
                if match_id == current_id:
                    # Same section resuming - this is intra-section content (part's content_after)
                    if after_lines:
                        sections_by_id[current_id].parts[-1].content_after = "\n".join(after_lines)
                    current_start = i
                    content_lines = []
                    after_lines = []
                    state = _ParseState.IN_SECTION
                else:
                    # Different section starting - this is inter-section content (section's content_after)
                    if after_lines:
                        sections_by_id[current_id].content_after = "\n".join(after_lines)
                    current_id = match_id
                    current_start = i
                    content_lines = []
                    after_lines = []
                    sections_by_id.setdefault(current_id, Section(id=current_id, parts=[]))
                    if current_id not in section_order:
                        section_order.append(current_id)
                    state = _ParseState.IN_SECTION
            else:
                after_lines.append(line)

    if state == _ParseState.IN_SECTION:
        raise ValueError(f"Unclosed section '{current_id}' starting at line {current_start}{file_suffix}")

    # Capture trailing content after last section
    if state == _ParseState.PAUSED and after_lines and current_id:
        sections_by_id[current_id].content_after = "\n".join(after_lines)

    return [sections_by_id[sid] for sid in section_order]


def has_sections(content: str, tool_name: str, config: CommentConfig) -> bool:
    return bool(_build_start_pattern(tool_name, config).search(content))


def extract_sections(
    content: str,
    tool_name: str,
    config: CommentConfig,
    filename: str = "",
) -> dict[str, str]:
    return {s.id: s.content for s in parse_sections(content, tool_name, config, filename)}


def compare_sections(
    baseline_content: str,
    current_content: str,
    tool_name: str,
    config: CommentConfig,
    skip: set[str] | None = None,
    filename: str = "",
) -> list[str]:
    """Return section IDs with changes (modified or removed), excluding skipped sections."""
    skip_ids = skip or set()
    baseline_secs = extract_sections(baseline_content, tool_name, config, filename)
    current_secs = extract_sections(current_content, tool_name, config, filename)
    return [
        sec_id
        for sec_id, baseline_text in baseline_secs.items()
        if sec_id not in skip_ids and baseline_text != current_secs.get(sec_id, "")
    ]


def changed_sections(
    baseline_content: str,
    current_content: str,
    tool_name: str,
    config: CommentConfig,
    skip: set[str] | None = None,
    filename: str = "",
) -> SectionChanges:
    """Return modified and missing sections separately."""
    skip_ids = skip or set()
    baseline_secs = extract_sections(baseline_content, tool_name, config, filename)
    current_secs = extract_sections(current_content, tool_name, config, filename)
    modified, missing = [], []
    for sec_id, baseline_text in baseline_secs.items():
        if sec_id in skip_ids:
            continue
        if sec_id not in current_secs:
            missing.append(sec_id)
        elif baseline_text != current_secs[sec_id]:
            modified.append(sec_id)
    return SectionChanges(modified=modified, missing=missing)


def wrap_section(content: str, section_id: str, tool_name: str, config: CommentConfig) -> str:
    start = _start_marker(tool_name, section_id, config)
    end = _end_marker(tool_name, section_id, config)
    return f"{start}\n{content}\n{end}"


def wrap_in_default_section(content: str, tool_name: str, config: CommentConfig) -> str:
    return wrap_section(content, "default", tool_name, config)


def _normalize_src_sections(src_sections: dict[str, str] | list[Section]) -> list[Section]:
    if isinstance(src_sections, dict):
        return [Section(id=sid, parts=[SectionPart(content, 0, 0)]) for sid, content in src_sections.items()]
    return src_sections


def _render_section_parts(
    parts: list[SectionPart],
    section_id: str,
    tool_name: str,
    config: CommentConfig,
) -> list[str]:
    result: list[str] = []
    for part in parts:
        result.append(_start_marker(tool_name, section_id, config))
        if part.content:
            result.append(part.content)
        result.append(_end_marker(tool_name, section_id, config))
        if part.content_after is not None:
            result.append(part.content_after)
    return result


def replace_sections(  # noqa: C901
    dest_content: str,
    src_sections: dict[str, str] | list[Section],
    tool_name: str,
    config: CommentConfig,
    skip_sections: list[str] | None = None,
    *,
    keep_deleted_sections: bool = False,
) -> str:
    """Replace sections in dest_content with src_sections, preserving user content."""
    skip = set(skip_sections or [])
    src_list = _normalize_src_sections(src_sections)
    src_by_id = {s.id: s for s in src_list}
    dest_parsed = parse_sections(dest_content, tool_name, config)

    # Capture dest's trailing content (content after last section) before processing
    dest_trailing: str | None = dest_parsed[-1].content_after if dest_parsed else None
    last_dest_id = dest_parsed[-1].id if dest_parsed else None

    # Collect preamble (lines before any section starts)
    start_pattern = _build_start_pattern(tool_name, config)
    preamble: list[str] = []
    for line in dest_content.split("\n"):
        if start_pattern.match(line):
            break
        preamble.append(line)

    result: list[str] = preamble.copy()
    seen_sections: set[str] = set()

    for dest_section in dest_parsed:
        sid = dest_section.id
        seen_sections.add(sid)
        is_last_dest_section = sid == last_dest_id

        if sid in skip:
            result.extend(_render_section_parts(dest_section.parts, sid, tool_name, config))
            if dest_section.content_after is not None and not is_last_dest_section:
                result.append(dest_section.content_after)
            continue

        if sid not in src_by_id:
            if keep_deleted_sections:
                result.extend(_render_section_parts(dest_section.parts, sid, tool_name, config))
                if dest_section.content_after is not None and not is_last_dest_section:
                    result.append(dest_section.content_after)
            continue

        src_section = src_by_id[sid]
        merged_parts: list[SectionPart] = []
        dest_len, src_len = len(dest_section.parts), len(src_section.parts)

        for i in range(max(dest_len, src_len)):
            if i < src_len:
                src_part = src_section.parts[i]
                has_more_parts = i + 1 < src_len
                # Only preserve intra-section content if source expects it
                if has_more_parts or src_part.content_after is not None:
                    # Dest has structure if it has a next part (i+1 exists)
                    dest_has_structure = i + 1 < dest_len
                    if dest_has_structure:
                        after = dest_section.parts[i].content_after
                    elif i < dest_len and dest_section.parts[i].content_after is not None:
                        after = dest_section.parts[i].content_after
                    else:
                        after = src_part.content_after
                else:
                    after = None
                merged_parts.append(SectionPart(src_part.content, 0, 0, after))
            else:
                logger.warning(f"Deleting extra dest part {i} for section '{sid}'")

        if src_len > dest_len:
            logger.warning(f"Appending {src_len - dest_len} extra src part(s) for section '{sid}'")

        result.extend(_render_section_parts(merged_parts, sid, tool_name, config))

        # Preserve inter-section content (skip trailing - it's appended at end)
        if dest_section.content_after is not None and not is_last_dest_section:
            result.append(dest_section.content_after)

    # Append new sections not in dest (skip source's content_after - use dest's trailing instead)
    for src_section in src_list:
        if src_section.id in seen_sections or src_section.id in skip:
            continue
        result.extend(_render_section_parts(src_section.parts, src_section.id, tool_name, config))

    # Append trailing content: dest's if updating, source's if initial copy
    if dest_trailing is not None:
        result.append(dest_trailing)
    elif not dest_parsed and src_list and src_list[-1].content_after is not None:
        result.append(src_list[-1].content_after)

    return "\n".join(result)


# Path-based convenience functions
def parse_sections_from_path(path: Path, tool_name: str) -> list[Section]:
    config = get_comment_config(path)
    return parse_sections(path.read_text(), tool_name, config, str(path))


def has_sections_in_path(path: Path, tool_name: str) -> bool:
    config = get_comment_config(path)
    return has_sections(path.read_text(), tool_name, config)


def extract_sections_from_path(path: Path, tool_name: str) -> dict[str, str]:
    config = get_comment_config(path)
    return extract_sections(path.read_text(), tool_name, config, str(path))
