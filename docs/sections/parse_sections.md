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

<!-- === DO_NOT_EDIT: pkg-ext parse_sections_changes === -->
### Changes

| Version | Change |
|---------|--------|
| 0.101.0 | Made public |
<!-- === OK_EDIT: pkg-ext parse_sections_changes === -->