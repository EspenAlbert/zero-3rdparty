from pathlib import Path

import pytest

from zero_3rdparty._internal.sections import (
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
    slug,
    wrap_in_default_section,
)

HASH_CONFIG = CommentConfig("#")
HTML_CONFIG = CommentConfig("<!--", " -->")


def test_slug():
    assert slug("hello world") == "hello_world"
    assert slug("HelloWorld") == "helloworld"
    assert slug("parse_config") == "parse_config"
    assert slug("Some.Thing!") == "something"
    assert slug("class_DumpYaml") == "class_dumpyaml"


JUSTFILE_CONTENT = """\
# header line

# === OK_EDIT: mytool header ===
# Custom variables

# === DO_NOT_EDIT: mytool standard ===
pre-push: lint test
# === OK_EDIT: mytool standard ===

# === DO_NOT_EDIT: mytool coverage ===
cov:
  uv run pytest --cov
# === OK_EDIT: mytool coverage ===
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
# === OK_EDIT: t inner ===
# === OK_EDIT: t outer ===
"""
    with pytest.raises(ValueError, match="Nested section"):
        parse_sections(nested, "t", HASH_CONFIG)

    unclosed = "# === DO_NOT_EDIT: t test ===\ncontent"
    with pytest.raises(ValueError, match="Unclosed section"):
        parse_sections(unclosed, "t", HASH_CONFIG)

    mismatched = """\
# === DO_NOT_EDIT: t sec1 ===
content
# === OK_EDIT: t sec2 ===
"""
    with pytest.raises(ValueError, match="Mismatched section end"):
        parse_sections(mismatched, "t", HASH_CONFIG)


def test_parse_sections_edge_cases():
    assert not parse_sections("plain content", "t", HASH_CONFIG)
    assert not parse_sections("# === OK_EDIT: t orphan ===\ncontent", "t", HASH_CONFIG)


def test_extract_and_has_sections():
    assert has_sections(JUSTFILE_CONTENT, "mytool", HASH_CONFIG)
    assert not has_sections("plain", "mytool", HASH_CONFIG)
    result = extract_sections(JUSTFILE_CONTENT, "mytool", HASH_CONFIG)
    assert result["standard"] == "pre-push: lint test"
    assert "cov:" in result["coverage"]


def test_wrap_in_default_section():
    result = wrap_in_default_section("content", "mytool", HASH_CONFIG)
    assert "DO_NOT_EDIT: mytool default" in result
    assert result.endswith("# === OK_EDIT: mytool default ===")


def test_replace_sections():
    dest = """\
# === DO_NOT_EDIT: t std ===
old
# === OK_EDIT: t std ==="""
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
    assert "OK_EDIT: t newid" in result3

    # deletes dest-only sections by default
    dest_only = """\
# === DO_NOT_EDIT: t custom ===
my stuff
# === OK_EDIT: t custom ==="""
    result4 = replace_sections(dest_only, {}, "t", HASH_CONFIG)
    assert "my stuff" not in result4
    assert "custom" not in result4

    # preserves dest-only sections if in skip_sections
    result5 = replace_sections(dest_only, {}, "t", HASH_CONFIG, skip_sections=["custom"])
    assert "my stuff" in result5

    # preserves dest-only sections with keep_deleted_sections=True
    result6 = replace_sections(dest_only, {}, "t", HASH_CONFIG, keep_deleted_sections=True)
    assert "my stuff" in result6


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
<!-- === OK_EDIT: pkg heading === -->
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
# === OK_EDIT: tool sec ===
""")
    assert has_sections_in_path(f, "tool")
    sections = parse_sections_from_path(f, "tool")
    assert sections[0].id == "sec"
    extracted = extract_sections_from_path(f, "tool")
    assert extracted["sec"] == "content here"


def test_replace_sections_with_empty_content():
    """Regression test: empty content should still produce valid sections with end markers."""
    dest = """\
# === DO_NOT_EDIT: t symbols ===
- old_symbol
# === OK_EDIT: t symbols ==="""
    # Replace with empty content
    result = replace_sections(dest, {"symbols": ""}, "t", HASH_CONFIG)

    # Must be parseable (no unclosed sections)
    sections = parse_sections(result, "t", HASH_CONFIG)
    assert len(sections) == 1
    assert sections[0].id == "symbols"
    assert sections[0].content == ""

    # Both markers must be present
    assert "DO_NOT_EDIT: t symbols" in result
    assert "OK_EDIT: t symbols" in result


def test_compare_sections():
    baseline = """\
# === DO_NOT_EDIT: t sec1 ===
original
# === OK_EDIT: t sec1 ===
# === DO_NOT_EDIT: t sec2 ===
unchanged
# === OK_EDIT: t sec2 ==="""
    # sec1 modified, sec2 unchanged
    current = """\
# === DO_NOT_EDIT: t sec1 ===
modified
# === OK_EDIT: t sec1 ===
# === DO_NOT_EDIT: t sec2 ===
unchanged
# === OK_EDIT: t sec2 ==="""
    assert compare_sections(baseline, current, "t", HASH_CONFIG) == ["sec1"]

    # sec1 removed (not in current)
    current_removed = """\
# === DO_NOT_EDIT: t sec2 ===
unchanged
# === OK_EDIT: t sec2 ==="""
    assert compare_sections(baseline, current_removed, "t", HASH_CONFIG) == ["sec1"]

    # skip sec1
    assert not compare_sections(baseline, current, "t", HASH_CONFIG, skip={"sec1"})
