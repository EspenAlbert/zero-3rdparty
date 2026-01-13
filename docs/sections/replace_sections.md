# replace_sections

<!-- === DO_NOT_EDIT: pkg-ext replace_sections_def === -->
## function: replace_sections
- [source](../../_internal/sections.py#L194)

```python
def replace_sections(dest_content: str, src_sections: dict[str, str], tool_name: str, config: CommentConfig, skip_sections: list[str] | None = None) -> str:
    ...
```

The type of the None singleton.
<!-- === OK_EDIT: pkg-ext replace_sections_def === -->

<!-- === DO_NOT_EDIT: pkg-ext replace_sections_example_replace_existing === -->
### Example: replace_existing

```python
result = replace_sections(
    dest_content="""\
# === DO_NOT_EDIT: t std ===
old content
# === OK_EDIT: t std ===""",
    src_sections={"std": "new content"},
    tool_name="t",
    config={"prefix": "#", "suffix": ""},
    skip_sections=None,
)
```
<!-- === OK_EDIT: pkg-ext replace_sections_example_replace_existing === -->

<!-- === DO_NOT_EDIT: pkg-ext replace_sections_example_skip_section === -->
### Example: skip_section

```python
result = replace_sections(
    dest_content="""\
# === DO_NOT_EDIT: t std ===
preserved
# === OK_EDIT: t std ===""",
    src_sections={"std": "would be replaced"},
    tool_name="t",
    config={"prefix": "#", "suffix": ""},
    skip_sections=["std"],
)
```
<!-- === OK_EDIT: pkg-ext replace_sections_example_skip_section === -->

<!-- === DO_NOT_EDIT: pkg-ext replace_sections_changes === -->
### Changes

| Version | Change |
|---------|--------|
| unreleased | Made public |
<!-- === OK_EDIT: pkg-ext replace_sections_changes === -->