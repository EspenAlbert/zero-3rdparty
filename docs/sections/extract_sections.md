# extract_sections

<!-- === DO_NOT_EDIT: pkg-ext extract_sections_def === -->
## function: extract_sections
- [source](../../_internal/sections.py#L162)

```python
def extract_sections(content: str, tool_name: str, config: CommentConfig) -> dict[str, str]:
    ...
```

The type of the None singleton.
<!-- === OK_EDIT: pkg-ext extract_sections_def === -->

<!-- === DO_NOT_EDIT: pkg-ext extract_sections_example_extract_from_justfile === -->
### Example: extract_from_justfile

```python
result = extract_sections(content='# header line\n\n# === OK_EDIT: mytool header ===\n# Custom variables\n\n# === DO_NOT_EDIT: mytool standard ===\npre-push: lint test\n# === OK_EDIT: mytool standard ===\n\n# === DO_NOT_EDIT: mytool coverage ===\ncov:\n  uv run pytest --cov\n# === OK_EDIT: mytool coverage ===\n', tool_name='mytool', config={'prefix': '#', 'suffix': ''})
```
<!-- === OK_EDIT: pkg-ext extract_sections_example_extract_from_justfile === -->

<!-- === DO_NOT_EDIT: pkg-ext extract_sections_changes === -->
### Changes

| Version | Change |
|---------|--------|
| unreleased | Made public |
<!-- === OK_EDIT: pkg-ext extract_sections_changes === -->