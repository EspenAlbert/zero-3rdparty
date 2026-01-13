# has_sections

<!-- === DO_NOT_EDIT: pkg-ext has_sections_def === -->
## function: has_sections
- [source](../../_internal/sections.py#L158)

```python
def has_sections(content: str, tool_name: str, config: CommentConfig) -> bool:
    ...
```

The type of the None singleton.
<!-- === OK_EDIT: pkg-ext has_sections_def === -->

<!-- === DO_NOT_EDIT: pkg-ext has_sections_example_has_sections_false === -->
### Example: has_sections_false

```python
result = has_sections(content='plain content without markers', tool_name='mytool', config={'prefix': '#', 'suffix': ''})
```
<!-- === OK_EDIT: pkg-ext has_sections_example_has_sections_false === -->

<!-- === DO_NOT_EDIT: pkg-ext has_sections_example_has_sections_true === -->
### Example: has_sections_true

```python
result = has_sections(content='# header line\n\n# === OK_EDIT: mytool header ===\n# Custom variables\n\n# === DO_NOT_EDIT: mytool standard ===\npre-push: lint test\n# === OK_EDIT: mytool standard ===\n\n# === DO_NOT_EDIT: mytool coverage ===\ncov:\n  uv run pytest --cov\n# === OK_EDIT: mytool coverage ===\n', tool_name='mytool', config={'prefix': '#', 'suffix': ''})
```
<!-- === OK_EDIT: pkg-ext has_sections_example_has_sections_true === -->

<!-- === DO_NOT_EDIT: pkg-ext has_sections_changes === -->
### Changes

| Version | Change |
|---------|--------|
| unreleased | Made public |
<!-- === OK_EDIT: pkg-ext has_sections_changes === -->