# parse_sections

<!-- === DO_NOT_EDIT: pkg-ext parse_sections_def === -->
## function: parse_sections
- [source](../../zero_3rdparty/_internal/sections.py#L125)
> **Since:** 0.101.0

```python
def parse_sections(content: str, tool_name: str, config: CommentConfig, filename: str = '') -> list[Section]:
    ...
```
<!-- === OK_EDIT: pkg-ext parse_sections_def === -->

Returns a list of `Section` objects, each containing one or more `SectionPart` entries. Sections can be "resumable" - the same section ID can pause (OK_EDIT) and resume (DO_NOT_EDIT) multiple times. User content in the gaps between parts is captured in `SectionPart.gap_after`.

<!-- === DO_NOT_EDIT: pkg-ext parse_sections_example_html_sections === -->
### Example: html_sections

```python
result = parse_sections(
    content="""\
<!-- === DO_NOT_EDIT: pkg heading === -->
# Title
<!-- === OK_EDIT: pkg heading === -->
""",
    tool_name="pkg",
    config={"prefix": "<!--", "suffix": " -->"},
    filename="index.html",
)
```
<!-- === OK_EDIT: pkg-ext parse_sections_example_html_sections === -->

<!-- === DO_NOT_EDIT: pkg-ext parse_sections_example_justfile_sections === -->
### Example: justfile_sections

```python
result = parse_sections(
    content="""\
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
""",
    tool_name="mytool",
    config={"prefix": "#", "suffix": ""},
    filename="justfile",
)
```
<!-- === OK_EDIT: pkg-ext parse_sections_example_justfile_sections === -->

### Example: resumable section with gaps

A section can be paused and resumed, allowing user content in the gaps:

```python
content = """\
# === DO_NOT_EDIT: path-sync job ===
name: CI Job
runs-on: ubuntu-latest
# === OK_EDIT: path-sync job ===
env:
  MY_SECRET: ${{ secrets.MY_SECRET }}  # user-customizable gap
# === DO_NOT_EDIT: path-sync job ===
steps:
  - uses: actions/checkout@v4
# === OK_EDIT: path-sync job ===
"""
result = parse_sections(content, "path-sync", CommentConfig("#"))
# result[0].parts[0].content = "name: CI Job\nruns-on: ubuntu-latest"
# result[0].parts[0].gap_after = "env:\n  MY_SECRET: ..."
# result[0].parts[1].content = "steps:\n  - uses: actions/checkout@v4"
```

<!-- === DO_NOT_EDIT: pkg-ext parse_sections_changes === -->
### Changes

| Version | Change |
|---------|--------|
| 0.101.0 | Made public |
<!-- === OK_EDIT: pkg-ext parse_sections_changes === -->
