from pathlib import Path

import pytest

from zero_3rdparty._internal.sections import (
    CommentConfig,
    Section,
    SectionPart,
    changed_sections,
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


def test_changed_sections():
    baseline = """\
# === DO_NOT_EDIT: t sec1 ===
original
# === OK_EDIT: t sec1 ===
# === DO_NOT_EDIT: t sec2 ===
unchanged
# === OK_EDIT: t sec2 ===
# === DO_NOT_EDIT: t sec3 ===
will be removed
# === OK_EDIT: t sec3 ==="""
    current = """\
# === DO_NOT_EDIT: t sec1 ===
modified
# === OK_EDIT: t sec1 ===
# === DO_NOT_EDIT: t sec2 ===
unchanged
# === OK_EDIT: t sec2 ==="""
    result = changed_sections(baseline, current, "t", HASH_CONFIG)
    assert result.modified == ["sec1"]
    assert result.missing == ["sec3"]

    result_skip = changed_sections(baseline, current, "t", HASH_CONFIG, skip={"sec1", "sec3"})
    assert result_skip.modified == []
    assert result_skip.missing == []


HYPHENATED_CONTENT = """\
# header

# === DO_NOT_EDIT: path-sync standard ===
pre-push: lint test
# === OK_EDIT: path-sync standard ===

# === DO_NOT_EDIT: path-sync pkg-ext ===
pkg-pre-change:
  uv run --group release pkg-ext pre-change
# === OK_EDIT: path-sync pkg-ext ===

# === DO_NOT_EDIT: path-sync my-custom-section ===
custom content
# === OK_EDIT: path-sync my-custom-section ===
"""


def test_parse_sections_with_hyphenated_ids():
    result = parse_sections(HYPHENATED_CONTENT, "path-sync", HASH_CONFIG)
    assert len(result) == 3
    ids = [s.id for s in result]
    assert "standard" in ids
    assert "pkg-ext" in ids
    assert "my-custom-section" in ids


def test_extract_sections_with_hyphenated_ids():
    assert has_sections(HYPHENATED_CONTENT, "path-sync", HASH_CONFIG)
    result = extract_sections(HYPHENATED_CONTENT, "path-sync", HASH_CONFIG)
    assert "standard" in result
    assert "pkg-ext" in result
    assert "my-custom-section" in result
    assert "--group release" in result["pkg-ext"]


def test_replace_sections_with_hyphenated_ids():
    dest = """\
# === DO_NOT_EDIT: path-sync pkg-ext ===
old content
# === OK_EDIT: path-sync pkg-ext ==="""
    result = replace_sections(dest, {"pkg-ext": "new content"}, "path-sync", HASH_CONFIG)
    assert "new content" in result
    assert "old content" not in result

    result_skip = replace_sections(dest, {"pkg-ext": "replaced"}, "path-sync", HASH_CONFIG, skip_sections=["pkg-ext"])
    assert "old content" in result_skip
    assert "replaced" not in result_skip


# ============================================================================
# Resumable Sections (OK_EDIT in the middle) - Feature Tests
# ============================================================================
# These tests demonstrate the desired behavior for t07-20: resumable sections
# where the same section ID can pause (OK_EDIT) and resume (DO_NOT_EDIT)
# allowing user content in the "gap" between.


RESUMABLE_SECTION_CONTENT = """\
# === DO_NOT_EDIT: path-sync job-snapshot-tests ===
plan-snapshot-tests:
  name: Terraform Examples Plan Snapshot Tests
  runs-on: ubuntu-latest
  if: ${{ vars.SKIP_SNAPSHOT_TESTS != 'true' }}
# === OK_EDIT: path-sync job-snapshot-tests ===
  env:
    # Module-specific: Add required cloud provider credentials here
    MONGODB_ATLAS_CLIENT_ID: ${{ secrets.MONGODB_ATLAS_CLIENT_ID }}
    MONGODB_ATLAS_CLIENT_SECRET: ${{ secrets.MONGODB_ATLAS_CLIENT_SECRET }}
# === DO_NOT_EDIT: path-sync job-snapshot-tests ===
  steps:
    - uses: actions/checkout@v4
    - name: Run snapshot tests
      run: make test-snapshot
# === OK_EDIT: path-sync job-snapshot-tests ===
"""


def test_parse_resumable_section():
    """Parse a section with OK_EDIT in the middle (pause/resume pattern)."""
    sections = parse_sections(RESUMABLE_SECTION_CONTENT, "path-sync", HASH_CONFIG)
    assert len(sections) == 1
    section = sections[0]
    assert section.id == "job-snapshot-tests"
    # Section should have 2 parts (before and after the gap)
    assert len(section.parts) == 2
    # First part: job header
    assert "runs-on: ubuntu-latest" in section.parts[0].content
    # Second part: steps
    assert "actions/checkout" in section.parts[1].content
    # Gap content (env) should NOT be in the section content
    assert "MONGODB_ATLAS_CLIENT_ID" not in section.content


def test_extract_resumable_section():
    """Extract sections should join parts or return list of parts."""
    result = extract_sections(RESUMABLE_SECTION_CONTENT, "path-sync", HASH_CONFIG)
    assert "job-snapshot-tests" in result
    # Content should be the managed parts joined, not including the gap
    content = result["job-snapshot-tests"]
    assert "runs-on: ubuntu-latest" in content
    assert "actions/checkout" in content
    assert "MONGODB_ATLAS_CLIENT_ID" not in content


RESUMABLE_DEST_CONTENT = """\
# === DO_NOT_EDIT: path-sync job-snapshot-tests ===
plan-snapshot-tests:
  name: Old Job Name
  runs-on: ubuntu-20.04
# === OK_EDIT: path-sync job-snapshot-tests ===
  env:
    MY_CUSTOM_VAR: ${{ secrets.MY_CUSTOM_VAR }}
    ANOTHER_SECRET: ${{ secrets.ANOTHER_SECRET }}
# === DO_NOT_EDIT: path-sync job-snapshot-tests ===
  steps:
    - uses: actions/checkout@v3
# === OK_EDIT: path-sync job-snapshot-tests ===
"""


def test_replace_resumable_section_preserves_gap():
    """Replace should update managed parts while preserving user gap content."""
    src_sections = [
        Section(
            id="job-snapshot-tests",
            parts=[
                SectionPart("plan-snapshot-tests:\n  name: New Job Name\n  runs-on: ubuntu-latest", 0, 0),
                SectionPart("  steps:\n    - uses: actions/checkout@v4", 0, 0),
            ],
        )
    ]
    result = replace_sections(RESUMABLE_DEST_CONTENT, src_sections, "path-sync", HASH_CONFIG)

    assert "name: New Job Name" in result
    assert "runs-on: ubuntu-latest" in result
    assert "actions/checkout@v4" in result
    assert "Old Job Name" not in result
    assert "ubuntu-20.04" not in result
    assert "checkout@v3" not in result
    # Gap content preserved from dest
    assert "MY_CUSTOM_VAR" in result
    assert "ANOTHER_SECRET" in result


RESUMABLE_MULTIPLE_GAPS = """\
# === DO_NOT_EDIT: path-sync workflow ===
name: CI
on: push
# === OK_EDIT: path-sync workflow ===
env:
  CUSTOM_ENV: value
# === DO_NOT_EDIT: path-sync workflow ===
jobs:
  build:
    runs-on: ubuntu-latest
# === OK_EDIT: path-sync workflow ===
    env:
      JOB_CUSTOM: value
# === DO_NOT_EDIT: path-sync workflow ===
    steps:
      - run: echo done
# === OK_EDIT: path-sync workflow ===
"""


def test_parse_resumable_section_multiple_gaps():
    """Parse section with multiple gaps (3 managed parts, 2 gaps)."""
    sections = parse_sections(RESUMABLE_MULTIPLE_GAPS, "path-sync", HASH_CONFIG)
    assert len(sections) == 1
    section = sections[0]
    assert section.id == "workflow"
    assert len(section.parts) == 3
    # Part 1: workflow header
    assert "on: push" in section.parts[0].content
    # Part 2: jobs definition
    assert "runs-on: ubuntu-latest" in section.parts[1].content
    # Part 3: steps
    assert "echo done" in section.parts[2].content


# ============================================================================
# Gap Content Capture - Tests for t07-07
# ============================================================================
# Key insight: When replacing into a NEW file, we need source's gap content
# as boilerplate/instructions. This means gaps must be captured during parse.


RESUMABLE_SOURCE_WITH_GAPS = """\
# === DO_NOT_EDIT: path-sync job ===
name: CI Job
runs-on: ubuntu-latest
# === OK_EDIT: path-sync job ===
# CUSTOMIZE: Add your environment variables here
# Example:
#   MY_VAR: ${{ secrets.MY_VAR }}
# === DO_NOT_EDIT: path-sync job ===
steps:
  - uses: actions/checkout@v4
# === OK_EDIT: path-sync job ===
"""


def test_parse_resumable_section_captures_gaps():
    """Gaps should be captured on each part for use in new file creation."""
    sections = parse_sections(RESUMABLE_SOURCE_WITH_GAPS, "path-sync", HASH_CONFIG)
    assert len(sections) == 1
    section = sections[0]
    assert section.id == "job"
    assert len(section.parts) == 2
    # Gap should be on the first part (content after its OK_EDIT)
    assert section.parts[0].content_after is not None
    assert "CUSTOMIZE: Add your environment variables" in section.parts[0].content_after
    # Last part has no gap after (None means no content_after was set)
    assert section.parts[1].content_after is None


def test_replace_resumable_section_new_file_includes_source_gaps():
    """When dest is empty/new, source gaps should be included as boilerplate."""
    src_sections = parse_sections(RESUMABLE_SOURCE_WITH_GAPS, "path-sync", HASH_CONFIG)

    # Empty destination - new file
    dest_content = ""
    result = replace_sections(dest_content, src_sections, "path-sync", HASH_CONFIG)

    # Managed content should be present
    assert "name: CI Job" in result
    assert "runs-on: ubuntu-latest" in result
    assert "actions/checkout@v4" in result

    # Source gap content should be included as boilerplate
    assert "CUSTOMIZE: Add your environment variables" in result
    assert "Example:" in result


def test_replace_resumable_section_existing_file_preserves_dest_gaps():
    """When dest exists with gaps, dest gaps should be preserved (not replaced by src gaps)."""
    src_sections = parse_sections(RESUMABLE_SOURCE_WITH_GAPS, "path-sync", HASH_CONFIG)

    dest_content = """\
# === DO_NOT_EDIT: path-sync job ===
name: Old Name
# === OK_EDIT: path-sync job ===
env:
  MY_SECRET: ${{ secrets.MY_SECRET }}
  ANOTHER_VAR: custom_value
# === DO_NOT_EDIT: path-sync job ===
steps:
  - uses: actions/checkout@v3
# === OK_EDIT: path-sync job ===
"""
    result = replace_sections(dest_content, src_sections, "path-sync", HASH_CONFIG)

    # Managed content from source
    assert "name: CI Job" in result
    assert "runs-on: ubuntu-latest" in result
    assert "actions/checkout@v4" in result

    # Old managed content replaced
    assert "Old Name" not in result
    assert "checkout@v3" not in result

    # Dest gap content preserved (not replaced by source gap)
    assert "MY_SECRET" in result
    assert "ANOTHER_VAR" in result
    # Source gap boilerplate NOT included (dest has its own)
    assert "CUSTOMIZE: Add your environment" not in result


def test_replace_simple_source_to_resumable_dest():
    """Source has 1 part, dest has 2 parts with gap - trailing deleted."""
    # Simple source (no gaps)
    simple_source = """\
# === DO_NOT_EDIT: path-sync job ===
name: Simple Job
runs-on: ubuntu-latest
steps:
  - run: echo hello
# === OK_EDIT: path-sync job ===
"""
    src_sections = parse_sections(simple_source, "path-sync", HASH_CONFIG)
    assert len(src_sections[0].parts) == 1  # Simple = 1 part

    # Resumable dest (has gap)
    resumable_dest = """\
# === DO_NOT_EDIT: path-sync job ===
name: Old Name
# === OK_EDIT: path-sync job ===
env:
  MY_VAR: value
# === DO_NOT_EDIT: path-sync job ===
steps:
  - run: old command
# === OK_EDIT: path-sync job ===
"""
    result = replace_sections(resumable_dest, src_sections, "path-sync", HASH_CONFIG)

    # Source content present
    assert "name: Simple Job" in result
    assert "echo hello" in result

    # Dest structure collapsed to simple (trailing parts + gap deleted)
    # The result should have only 1 DO_NOT_EDIT/OK_EDIT pair
    assert result.count("DO_NOT_EDIT: path-sync job") == 1
    assert result.count("OK_EDIT: path-sync job") == 1

    # Gap content gone (source didn't have gaps)
    assert "MY_VAR" not in result


def test_replace_resumable_source_to_simple_dest():
    """Source has 2 parts with gap, dest has 1 part - extra parts appended."""
    src_sections = parse_sections(RESUMABLE_SOURCE_WITH_GAPS, "path-sync", HASH_CONFIG)
    assert len(src_sections[0].parts) == 2  # Resumable = 2 parts
    assert src_sections[0].parts[0].content_after  # First part has content_after

    # Simple dest (no gaps)
    simple_dest = """\
# === DO_NOT_EDIT: path-sync job ===
name: Old Simple Job
# === OK_EDIT: path-sync job ===
"""
    result = replace_sections(simple_dest, src_sections, "path-sync", HASH_CONFIG)

    # All source parts should be present
    assert "name: CI Job" in result
    assert "runs-on: ubuntu-latest" in result
    assert "actions/checkout@v4" in result

    # Structure expanded: should have 2 DO_NOT_EDIT/OK_EDIT pairs now
    assert result.count("DO_NOT_EDIT: path-sync job") == 2
    assert result.count("OK_EDIT: path-sync job") == 2

    # Source content_after included (dest didn't have any, so use source boilerplate)
    assert "CUSTOMIZE: Add your environment" in result


def test_parse_section_captures_trailing_content():
    """Trailing content after the final OK_EDIT IS captured in Section.content_after.

    This allows user content after a section to be preserved during replace_sections.
    """
    content_with_trailing = """\
# === DO_NOT_EDIT: path-sync job ===
name: Test Job
# === OK_EDIT: path-sync job ===
# This trailing content after final OK_EDIT
# IS captured in section.content_after
extra_key: value
"""
    sections = parse_sections(content_with_trailing, "path-sync", HASH_CONFIG)
    assert len(sections) == 1
    section = sections[0]
    assert len(section.parts) == 1
    # Part's content_after is None (no resumable gap)
    assert section.parts[0].content_after is None
    # Section's content_after captures trailing content
    assert section.content_after is not None
    assert "trailing content" in section.content_after
    assert "extra_key" in section.content_after
    # Only managed content is in the section content
    assert "name: Test Job" in section.content
    assert "trailing content" not in section.content


def test_replace_empty_dest_gap_preserved_when_structure_exists():
    """When dest has gap structure (2+ parts), empty gap is preserved (user cleared template).

    If the user deliberately removes the template content but keeps the gap structure
    (markers exist), we preserve their empty gap and don't re-inject the source template.
    """
    source_with_gap = """\
# === DO_NOT_EDIT: path-sync job ===
name: Source Job
# === OK_EDIT: path-sync job ===
# Default env vars - customize as needed:
#   MY_VAR: value
# === DO_NOT_EDIT: path-sync job ===
steps:
  - run: echo hello
# === OK_EDIT: path-sync job ===
"""
    # Dest has same structure (2 parts) but with EMPTY gap (one blank line - user cleared template)
    dest_with_empty_gap = """\
# === DO_NOT_EDIT: path-sync job ===
name: Dest Job
# === OK_EDIT: path-sync job ===

# === DO_NOT_EDIT: path-sync job ===
steps:
  - run: old command
# === OK_EDIT: path-sync job ===
"""
    src_sections = parse_sections(source_with_gap, "path-sync", HASH_CONFIG)
    assert src_sections[0].parts[0].content_after  # Source has gap
    assert len(src_sections[0].parts) == 2

    dest_sections = parse_sections(dest_with_empty_gap, "path-sync", HASH_CONFIG)
    # Dest has one blank line as gap (represented as "" when joined)
    assert dest_sections[0].parts[0].content_after == ""
    assert len(dest_sections[0].parts) == 2  # But dest HAS the structure

    result = replace_sections(dest_with_empty_gap, src_sections, "path-sync", HASH_CONFIG)

    # Source managed content used
    assert "name: Source Job" in result
    assert "echo hello" in result
    # Dest empty gap preserved (source template NOT injected)
    assert "Default env vars" not in result
    assert "MY_VAR" not in result


def test_replace_simple_dest_gets_source_gap_as_boilerplate():
    """When dest has NO gap structure (1 part), source gap is used as boilerplate.

    This is the case when expanding a simple section to resumable - the source
    gap content serves as template/instructions for the user.
    """
    source_with_gap = """\
# === DO_NOT_EDIT: path-sync job ===
name: Source Job
# === OK_EDIT: path-sync job ===
# Default env vars - customize as needed:
#   MY_VAR: value
# === DO_NOT_EDIT: path-sync job ===
steps:
  - run: echo hello
# === OK_EDIT: path-sync job ===
"""
    # Dest is SIMPLE (1 part, no gap structure)
    simple_dest = """\
# === DO_NOT_EDIT: path-sync job ===
name: Old Simple Job
# === OK_EDIT: path-sync job ===
"""
    src_sections = parse_sections(source_with_gap, "path-sync", HASH_CONFIG)
    assert len(src_sections[0].parts) == 2  # Source has 2 parts

    dest_sections = parse_sections(simple_dest, "path-sync", HASH_CONFIG)
    assert len(dest_sections[0].parts) == 1  # Dest has 1 part (no gap structure)

    result = replace_sections(simple_dest, src_sections, "path-sync", HASH_CONFIG)

    # Source managed content used
    assert "name: Source Job" in result
    assert "echo hello" in result
    # Source gap used as boilerplate (dest had no structure)
    assert "Default env vars" in result
    assert "MY_VAR" in result


# ============================================================================
# Inter-Section and Trailing Content - Tests for t07-08
# ============================================================================
# These tests verify that content BETWEEN sections and content AFTER the last
# section is preserved during replace_sections.


INTER_SECTION_CONTENT = """\
# Preamble content

# === DO_NOT_EDIT: tool section_a ===
content a
# === OK_EDIT: tool section_a ===

### User notes between sections
This content is between section_a and section_b.

# === DO_NOT_EDIT: tool section_b ===
content b
# === OK_EDIT: tool section_b ===

Trailing content after all sections.
"""


def test_parse_inter_section_content():
    """Content between sections should be captured in Section.content_after."""
    sections = parse_sections(INTER_SECTION_CONTENT, "tool", HASH_CONFIG)
    assert len(sections) == 2
    section_a = sections[0]
    section_b = sections[1]

    assert section_a.id == "section_a"
    assert section_b.id == "section_b"

    # section_a's content_after captures the inter-section content
    assert section_a.content_after is not None
    assert "User notes between sections" in section_a.content_after
    assert "between section_a and section_b" in section_a.content_after

    # section_b's content_after captures trailing content
    assert section_b.content_after is not None
    assert "Trailing content after all sections" in section_b.content_after


def test_replace_preserves_inter_section_content():
    """replace_sections should preserve user content between sections."""
    src_sections = [
        Section(id="section_a", parts=[SectionPart("new content a", 0, 0)]),
        Section(id="section_b", parts=[SectionPart("new content b", 0, 0)]),
    ]
    result = replace_sections(INTER_SECTION_CONTENT, src_sections, "tool", HASH_CONFIG)

    # Managed content updated
    assert "new content a" in result
    assert "new content b" in result
    assert "content a" not in result or "new content a" in result

    # Preamble preserved
    assert "Preamble content" in result

    # Inter-section content preserved
    assert "User notes between sections" in result
    assert "between section_a and section_b" in result

    # Trailing content preserved
    assert "Trailing content after all sections" in result


def test_replace_preserves_trailing_content():
    """Trailing content after the last section should be preserved."""
    dest = """\
# === DO_NOT_EDIT: tool sec ===
old content
# === OK_EDIT: tool sec ===

User documentation at the end of the file.
More trailing content here.
"""
    src_sections = [Section(id="sec", parts=[SectionPart("new content", 0, 0)])]
    result = replace_sections(dest, src_sections, "tool", HASH_CONFIG)

    # Managed content updated
    assert "new content" in result
    assert "old content" not in result

    # Trailing content preserved
    assert "User documentation at the end of the file" in result
    assert "More trailing content here" in result


def test_replace_new_file_uses_source_trailing_content():
    """When dest is empty, source's content_after is used as template."""
    src_sections = [
        Section(
            id="sec",
            parts=[SectionPart("managed content", 0, 0)],
            content_after="# Add your custom content here",
        )
    ]
    result = replace_sections("", src_sections, "tool", HASH_CONFIG)

    assert "managed content" in result
    assert "Add your custom content here" in result


def test_replace_dest_trailing_content_preserved_over_source():
    """Dest's trailing content takes precedence over source's."""
    src_sections = [
        Section(
            id="sec",
            parts=[SectionPart("new managed", 0, 0)],
            content_after="# Source template trailing",
        )
    ]
    dest = """\
# === DO_NOT_EDIT: tool sec ===
old managed
# === OK_EDIT: tool sec ===

My custom trailing content.
"""
    result = replace_sections(dest, src_sections, "tool", HASH_CONFIG)

    assert "new managed" in result
    # Dest trailing preserved
    assert "My custom trailing content" in result
    # Source trailing NOT injected
    assert "Source template trailing" not in result


def test_replace_empty_dest_trailing_preserved():
    """If user cleared trailing content (empty), preserve empty (don't inject source)."""
    src_sections = [
        Section(
            id="sec",
            parts=[SectionPart("new managed", 0, 0)],
            content_after="# Source template",
        )
    ]
    # Dest exists but has no trailing content (user may have removed it)
    dest = """\
# === DO_NOT_EDIT: tool sec ===
old managed
# === OK_EDIT: tool sec ==="""
    result = replace_sections(dest, src_sections, "tool", HASH_CONFIG)

    assert "new managed" in result
    # No trailing content should be present (user's empty trailing preserved)
    assert "Source template" not in result


def test_parse_multiple_sections_each_has_content_after():
    """Each section captures its own content_after until next section or EOF."""
    content = """\
# preamble
# === DO_NOT_EDIT: t a ===
a content
# === OK_EDIT: t a ===
after a
# === DO_NOT_EDIT: t b ===
b content
# === OK_EDIT: t b ===
after b
# === DO_NOT_EDIT: t c ===
c content
# === OK_EDIT: t c ===
after c (trailing)
"""
    sections = parse_sections(content, "t", HASH_CONFIG)
    assert len(sections) == 3

    assert sections[0].id == "a"
    assert sections[0].content_after is not None
    assert "after a" in sections[0].content_after
    assert "after b" not in sections[0].content_after

    assert sections[1].id == "b"
    assert sections[1].content_after is not None
    assert "after b" in sections[1].content_after
    assert "after c" not in sections[1].content_after

    assert sections[2].id == "c"
    assert sections[2].content_after is not None
    assert "after c (trailing)" in sections[2].content_after


# ============================================================================
# Idempotency Tests
# ============================================================================
# Verify that running replace_sections multiple times produces the same result.


def test_replace_sections_idempotent_simple():
    """Running replace_sections twice with same source produces identical output."""
    dest = """\
# preamble
# === DO_NOT_EDIT: t sec ===
old content
# === OK_EDIT: t sec ===
trailing content
"""
    src = {"sec": "new content"}
    result1 = replace_sections(dest, src, "t", HASH_CONFIG)
    result2 = replace_sections(result1, src, "t", HASH_CONFIG)
    assert result1 == result2


def test_replace_sections_idempotent_with_inter_section():
    """Idempotency with inter-section content between multiple sections."""
    dest = """\
# preamble

# === DO_NOT_EDIT: t a ===
content a
# === OK_EDIT: t a ===

User notes between sections.

# === DO_NOT_EDIT: t b ===
content b
# === OK_EDIT: t b ===

Trailing content.
"""
    src = {"a": "new a", "b": "new b"}
    result1 = replace_sections(dest, src, "t", HASH_CONFIG)
    result2 = replace_sections(result1, src, "t", HASH_CONFIG)
    assert result1 == result2
    # Verify content is preserved
    assert "User notes between sections" in result2
    assert "Trailing content" in result2


def test_replace_sections_idempotent_resumable():
    """Idempotency with resumable sections (intra-section gaps)."""
    dest = """\
# === DO_NOT_EDIT: t job ===
name: CI
# === OK_EDIT: t job ===
env:
  MY_VAR: value
# === DO_NOT_EDIT: t job ===
steps:
  - run: echo done
# === OK_EDIT: t job ===
"""
    src_sections = [
        Section(
            id="job",
            parts=[
                SectionPart("name: CI Updated", 0, 0),
                SectionPart("steps:\n  - run: echo updated", 0, 0),
            ],
        )
    ]
    result1 = replace_sections(dest, src_sections, "t", HASH_CONFIG)
    result2 = replace_sections(result1, src_sections, "t", HASH_CONFIG)
    assert result1 == result2
    # Verify gap content preserved
    assert "MY_VAR" in result2


def test_replace_sections_preserves_single_blank_line_between_sections():
    """Single blank line between sections should be preserved during replacement.

    This was a regression where a single blank line (content_after="") was lost
    because the truthy check `if content_after:` returned False for empty string.
    """
    # Source with blank line between sections
    source = """\
<!-- === DO_NOT_EDIT: pkg-ext header === -->
# header content
<!-- === OK_EDIT: pkg-ext header === -->

<!-- === DO_NOT_EDIT: pkg-ext symbols === -->
- symbol1
<!-- === OK_EDIT: pkg-ext symbols === -->
"""
    # Dest with blank line between sections (same structure)
    dest = """\
<!-- === DO_NOT_EDIT: pkg-ext header === -->
# old header
<!-- === OK_EDIT: pkg-ext header === -->

<!-- === DO_NOT_EDIT: pkg-ext symbols === -->
- old symbol
<!-- === OK_EDIT: pkg-ext symbols === -->
"""
    src_sections = parse_sections(source, "pkg-ext", HTML_CONFIG)
    result = replace_sections(dest, src_sections, "pkg-ext", HTML_CONFIG)

    # Verify content was updated
    assert "# header content" in result
    assert "- symbol1" in result
    assert "# old header" not in result

    # Verify blank line between sections is preserved
    lines = result.split("\n")
    header_end_idx = next(i for i, line in enumerate(lines) if "OK_EDIT: pkg-ext header" in line)
    symbols_start_idx = next(i for i, line in enumerate(lines) if "DO_NOT_EDIT: pkg-ext symbols" in line)
    # There should be exactly one blank line between them
    assert symbols_start_idx == header_end_idx + 2  # +1 for blank line, +1 for symbols line
    assert lines[header_end_idx + 1] == ""  # The blank line


def test_replace_new_sections_preserves_dest_trailing():
    """When adding new sections from source, preserve dest's trailing content."""
    dest = """\
# === DO_NOT_EDIT: t standard ===
old content
# === OK_EDIT: t standard ===
# dest trailing
dest-recipe:
    echo "keep me"
"""
    src = [
        Section(id="core", parts=[SectionPart("core content", 0, 0)]),
        Section(
            id="checks",
            parts=[SectionPart("checks content", 0, 0)],
            content_after="# source trailing\nsrc-recipe:\n    echo source",
        ),
    ]
    result = replace_sections(dest, src, "t", HASH_CONFIG)

    assert "core content" in result
    assert "checks content" in result
    assert "dest trailing" in result
    assert "keep me" in result
    assert "source trailing" not in result
    assert "echo source" not in result


def test_replace_sections_idempotent_full_document():
    """Idempotency test for a realistic document with all features."""
    dest = """\
# Document Title

Some preamble text.

# === DO_NOT_EDIT: tool header ===
## Generated Header
# === OK_EDIT: tool header ===

### User Section

Custom user content here.

# === DO_NOT_EDIT: tool body ===
Part 1 of body
# === OK_EDIT: tool body ===
# Customize this part:
#   option: value
# === DO_NOT_EDIT: tool body ===
Part 2 of body
# === OK_EDIT: tool body ===

# === DO_NOT_EDIT: tool footer ===
Generated footer
# === OK_EDIT: tool footer ===

Final notes at end of document.
"""
    src_sections = [
        Section(id="header", parts=[SectionPart("## Updated Header", 0, 0)]),
        Section(
            id="body",
            parts=[
                SectionPart("Part 1 updated", 0, 0),
                SectionPart("Part 2 updated", 0, 0),
            ],
        ),
        Section(id="footer", parts=[SectionPart("Updated footer", 0, 0)]),
    ]
    result1 = replace_sections(dest, src_sections, "tool", HASH_CONFIG)
    result2 = replace_sections(result1, src_sections, "tool", HASH_CONFIG)
    result3 = replace_sections(result2, src_sections, "tool", HASH_CONFIG)

    assert result1 == result2 == result3

    # Verify all user content preserved
    assert "Document Title" in result3
    assert "Some preamble text" in result3
    assert "User Section" in result3
    assert "Custom user content" in result3
    assert "Customize this part" in result3
    assert "Final notes at end" in result3
