# wrap_section

<!-- === DO_NOT_EDIT: pkg-ext wrap_section_def === -->
## function: wrap_section
- [source](../../_internal/sections.py#L184)

```python
def wrap_section(content: str, section_id: str, tool_name: str, config: CommentConfig) -> str:
    ...
```

The type of the None singleton.
<!-- === OK_EDIT: pkg-ext wrap_section_def === -->

<!-- === DO_NOT_EDIT: pkg-ext wrap_section_example_wrap_with_custom_id === -->
### Example: wrap_with_custom_id

```python
result = wrap_section(content='my content here', section_id='custom_section', tool_name='mytool', config={'prefix': '#', 'suffix': ''})
```
<!-- === OK_EDIT: pkg-ext wrap_section_example_wrap_with_custom_id === -->

<!-- === DO_NOT_EDIT: pkg-ext wrap_section_changes === -->
### Changes

| Version | Change |
|---------|--------|
| unreleased | Made public |
<!-- === OK_EDIT: pkg-ext wrap_section_changes === -->