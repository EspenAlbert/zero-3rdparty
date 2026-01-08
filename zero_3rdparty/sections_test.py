from pathlib import Path

import pytest

from zero_3rdparty.sections import (
    CommentConfig,
    compare_sections,
    extract_sections,
    extract_sections_from_path,
    get_comment_config,
    has_sections,
    has_sections_in_path,
    parse_sections,
    parse_sections_from_path,
    replace_sections,
    wrap_in_default_section,
)

HASH_CONFIG = CommentConfig("#")
HTML_CONFIG = CommentConfig("<!--", " -->")

JUSTFILE_CONTENT = """\
# header line

# === OK_EDIT ===
# Custom variables

# === DO_NOT_EDIT: mytool standard ===
pre-push: lint test
# === OK_EDIT ===

# === DO_NOT_EDIT: mytool coverage ===
cov:
  uv run pytest --cov
# === OK_EDIT ===
"""


def test_parse_sections():
    result = parse_sections(JUSTFILE_CONTENT, "mytool", HASH_CONFIG)
    assert len(result) == 2
    assert result[0].id == "standard"
    assert result[0].content == "pre-push: lint test"
    assert result[0].start_line == 5
    assert result[0].end_line == 7
    assert result[1].id == "coverage"
    assert "uv run pytest --cov" in result[1].content


def test_parse_sections_errors():
    nested = """\
# === DO_NOT_EDIT: t outer ===
# === DO_NOT_EDIT: t inner ===
# === OK_EDIT ===
# === OK_EDIT ===
"""
    with pytest.raises(ValueError, match="Nested section"):
        parse_sections(nested, "t", HASH_CONFIG)

    unclosed = "# === DO_NOT_EDIT: t test ===\ncontent"
    with pytest.raises(ValueError, match="Unclosed section"):
        parse_sections(unclosed, "t", HASH_CONFIG)


def test_parse_sections_edge_cases():
    assert parse_sections("plain content", "t", HASH_CONFIG) == []
    assert parse_sections("# === OK_EDIT ===\ncontent", "t", HASH_CONFIG) == []


def test_extract_and_has_sections():
    assert has_sections(JUSTFILE_CONTENT, "mytool", HASH_CONFIG)
    assert not has_sections("plain", "mytool", HASH_CONFIG)
    result = extract_sections(JUSTFILE_CONTENT, "mytool", HASH_CONFIG)
    assert result["standard"] == "pre-push: lint test"
    assert "cov:" in result["coverage"]


def test_wrap_in_default_section():
    result = wrap_in_default_section("content", "mytool", HASH_CONFIG)
    assert "DO_NOT_EDIT: mytool default" in result
    assert result.endswith("# === OK_EDIT ===")


def test_replace_sections():
    dest = """\
# === DO_NOT_EDIT: t std ===
old
# === OK_EDIT ==="""
    result = replace_sections(dest, {"std": "new"}, "t", HASH_CONFIG)
    assert "new" in result
    assert "old" not in result

    # skip_sections preserves dest content
    result2 = replace_sections(dest, {"std": "replaced"}, "t", HASH_CONFIG, skip_sections=["std"])
    assert "old" in result2
    assert "replaced" not in result2

    # adds new sections
    result3 = replace_sections("# plain", {"newid": "content"}, "t", HASH_CONFIG)
    assert "DO_NOT_EDIT: t newid" in result3

    # preserves dest-only sections
    dest_only = """\
# === DO_NOT_EDIT: t custom ===
my stuff
# === OK_EDIT ==="""
    result4 = replace_sections(dest_only, {}, "t", HASH_CONFIG)
    assert "my stuff" in result4


def test_get_comment_config():
    assert get_comment_config(Path("test.py")).prefix == "#"
    assert get_comment_config(Path("test.md")).suffix == " -->"
    assert get_comment_config("justfile").prefix == "#"
    assert get_comment_config(Path("x.ts")).prefix == "//"

    override = CommentConfig("%%")
    assert get_comment_config(Path("test.py"), override).prefix == "%%"

    with pytest.raises(ValueError, match="No comment config"):
        get_comment_config(Path("unknown.xyz"))


def test_html_comment_markers():
    content = """\
<!-- === DO_NOT_EDIT: pkg heading === -->
# Title
<!-- === OK_EDIT === -->
"""
    sections = parse_sections(content, "pkg", HTML_CONFIG)
    assert len(sections) == 1
    assert sections[0].id == "heading"
    assert sections[0].content == "# Title"

    result = replace_sections(content, {"heading": "# New Title"}, "pkg", HTML_CONFIG)
    assert "# New Title" in result


def test_path_based_functions(tmp_path: Path):
    f = tmp_path / "test.py"
    f.write_text("""\
# === DO_NOT_EDIT: tool sec ===
content here
# === OK_EDIT ===
""")
    assert has_sections_in_path(f, "tool")
    sections = parse_sections_from_path(f, "tool")
    assert sections[0].id == "sec"
    extracted = extract_sections_from_path(f, "tool")
    assert extracted["sec"] == "content here"


def test_compare_sections():
    baseline = """\
# === DO_NOT_EDIT: t sec1 ===
original
# === OK_EDIT ===
# === DO_NOT_EDIT: t sec2 ===
unchanged
# === OK_EDIT ==="""
    # sec1 modified, sec2 unchanged
    current = """\
# === DO_NOT_EDIT: t sec1 ===
modified
# === OK_EDIT ===
# === DO_NOT_EDIT: t sec2 ===
unchanged
# === OK_EDIT ==="""
    assert compare_sections(baseline, current, "t", HASH_CONFIG) == ["sec1"]

    # sec1 removed (not in current)
    current_removed = """\
# === DO_NOT_EDIT: t sec2 ===
unchanged
# === OK_EDIT ==="""
    assert compare_sections(baseline, current_removed, "t", HASH_CONFIG) == ["sec1"]

    # skip sec1
    assert compare_sections(baseline, current, "t", HASH_CONFIG, skip={"sec1"}) == []
