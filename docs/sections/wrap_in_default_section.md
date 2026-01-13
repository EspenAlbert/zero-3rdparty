# wrap_in_default_section

<!-- === DO_NOT_EDIT: pkg-ext wrap_in_default_section_def === -->
## function: wrap_in_default_section
- [source](../../_internal/sections.py#L190)

```python
def wrap_in_default_section(content: str, tool_name: str, config: CommentConfig) -> str:
    ...
```

The type of the None singleton.
<!-- === OK_EDIT: pkg-ext wrap_in_default_section_def === -->

<!-- === DO_NOT_EDIT: pkg-ext wrap_in_default_section_example_wrap_simple_content === -->
### Example: wrap_simple_content

```python
result = wrap_in_default_section(content='my content here', tool_name='mytool', config={'prefix': '#', 'suffix': ''})
```
<!-- === OK_EDIT: pkg-ext wrap_in_default_section_example_wrap_simple_content === -->

<!-- === DO_NOT_EDIT: pkg-ext wrap_in_default_section_changes === -->
### Changes

| Version | Change |
|---------|--------|
| unreleased | Made public |
<!-- === OK_EDIT: pkg-ext wrap_in_default_section_changes === -->