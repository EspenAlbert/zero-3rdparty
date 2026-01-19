# replace_sections

<!-- === DO_NOT_EDIT: pkg-ext replace_sections_def === -->
## function: replace_sections
- [source](../../zero_3rdparty/_internal/sections.py#L233)
> **Since:** 0.101.0

```python
def replace_sections(dest_content: str, src_sections: dict[str, str], tool_name: str, config: CommentConfig, skip_sections: list[str] | None = None, *, keep_deleted_sections: bool = False) -> str:
    ...
```

Replace sections in dest_content with src_sections.

Args:
    dest_content: The destination content containing sections to update
    src_sections: Dict mapping section IDs to their new content
    tool_name: The tool name used in section markers
    config: Comment configuration for the file type
    skip_sections: Section IDs to preserve unchanged (not replaced, not deleted)
    keep_deleted_sections: If True, preserve sections not in src_sections.
        If False (default), delete sections not in src_sections (unless skipped).

New sections from src_sections are always added at the end.
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
    keep_deleted_sections=False,
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
    keep_deleted_sections=False,
)
```
<!-- === OK_EDIT: pkg-ext replace_sections_example_skip_section === -->

<!-- === DO_NOT_EDIT: pkg-ext replace_sections_changes === -->
### Changes

| Version | Change |
|---------|--------|
| 0.101.0 | Made public |
<!-- === OK_EDIT: pkg-ext replace_sections_changes === -->