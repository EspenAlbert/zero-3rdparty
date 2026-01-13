# parse_sections

<!-- === DO_NOT_EDIT: pkg-ext parse_sections_def === -->
## function: parse_sections
- [source](../../_internal/sections.py#L116)

```python
def parse_sections(content: str, tool_name: str, config: CommentConfig) -> list[Section]:
    ...
```

The type of the None singleton.
<!-- === OK_EDIT: pkg-ext parse_sections_def === -->

<!-- === DO_NOT_EDIT: pkg-ext parse_sections_example_justfile_sections === -->
### Example: justfile_sections

```python
result = parse_sections(content='# header line\n\n# === OK_EDIT: mytool header ===\n# Custom variables\n\n# === DO_NOT_EDIT: mytool standard ===\npre-push: lint test\n# === OK_EDIT: mytool standard ===\n\n# === DO_NOT_EDIT: mytool coverage ===\ncov:\n  uv run pytest --cov\n# === OK_EDIT: mytool coverage ===\n', tool_name='mytool', config={'prefix': '#', 'suffix': ''}, expected_section_count=2, expected_first_id='standard', expected_first_content='pre-push: lint test')
```
<!-- === OK_EDIT: pkg-ext parse_sections_example_justfile_sections === -->

<!-- === DO_NOT_EDIT: pkg-ext parse_sections_changes === -->
### Changes

| Version | Change |
|---------|--------|
| unreleased | Made public |
<!-- === OK_EDIT: pkg-ext parse_sections_changes === -->
<!-- === DO_NOT_EDIT: pkg-ext parse_sections_example_html_sections === -->
### Example: html_sections

```python
result = parse_sections(content='<!-- === DO_NOT_EDIT: pkg heading === -->\n# Title\n<!-- === OK_EDIT: pkg heading === -->\n', tool_name='pkg', config={'prefix': '<!--', 'suffix': ' -->'}, expected_section_count=1, expected_first_id='heading', expected_first_content='# Title')
```
<!-- === OK_EDIT: pkg-ext parse_sections_example_html_sections === -->