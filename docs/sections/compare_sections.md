# compare_sections

<!-- === DO_NOT_EDIT: pkg-ext compare_sections_def === -->
## function: compare_sections
- [source](../../_internal/sections.py#L166)

```python
def compare_sections(baseline_content: str, current_content: str, tool_name: str, config: CommentConfig, skip: set[str] | None = None) -> list[str]:
    ...
```

The type of the None singleton.
<!-- === OK_EDIT: pkg-ext compare_sections_def === -->

<!-- === DO_NOT_EDIT: pkg-ext compare_sections_example_detect_modified_section === -->
### Example: detect_modified_section
Detect when sec1 was modified between baseline and current

```python
result = compare_sections(baseline_content='# === DO_NOT_EDIT: t sec1 ===\noriginal\n# === OK_EDIT: t sec1 ===\n# === DO_NOT_EDIT: t sec2 ===\nunchanged\n# === OK_EDIT: t sec2 ===', current_content='# === DO_NOT_EDIT: t sec1 ===\nmodified\n# === OK_EDIT: t sec1 ===\n# === DO_NOT_EDIT: t sec2 ===\nunchanged\n# === OK_EDIT: t sec2 ===', tool_name='t', config={'prefix': '#', 'suffix': ''}, skip=None)
```
<!-- === OK_EDIT: pkg-ext compare_sections_example_detect_modified_section === -->

<!-- === DO_NOT_EDIT: pkg-ext compare_sections_example_skip_section_in_compare === -->
### Example: skip_section_in_compare
Skip sec1 from comparison

```python
result = compare_sections(baseline_content='# === DO_NOT_EDIT: t sec1 ===\noriginal\n# === OK_EDIT: t sec1 ===', current_content='# === DO_NOT_EDIT: t sec1 ===\nmodified\n# === OK_EDIT: t sec1 ===', tool_name='t', config={'prefix': '#', 'suffix': ''}, skip={'sec1'})
```
<!-- === OK_EDIT: pkg-ext compare_sections_example_skip_section_in_compare === -->

<!-- === DO_NOT_EDIT: pkg-ext compare_sections_changes === -->
### Changes

| Version | Change |
|---------|--------|
| unreleased | Made public |
<!-- === OK_EDIT: pkg-ext compare_sections_changes === -->