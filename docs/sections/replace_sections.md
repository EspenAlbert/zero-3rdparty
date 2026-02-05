# replace_sections

<!-- === DO_NOT_EDIT: pkg-ext replace_sections_def === -->
## function: replace_sections
- [source](../../zero_3rdparty/_internal/sections.py#L314)
> **Since:** 0.101.0

```python
def replace_sections(dest_content: str, src_sections: dict[str, str] | list[Section], tool_name: str, config: CommentConfig, skip_sections: list[str] | None = None, *, keep_deleted_sections: bool = False) -> str:
    ...
```

Replace sections in dest_content with src_sections, preserving gap content.
<!-- === OK_EDIT: pkg-ext replace_sections_def === -->

### Gap Content Behavior

When a section has multiple parts (resumable sections), the function handles "gaps" (user content between parts) as follows:

- **Existing dest with gaps**: Dest gap content is preserved, source gaps are ignored
- **Empty dest gap**: Source gap is used as boilerplate template
- **New file (no dest sections)**: Source gaps are included as default content
- **Source has fewer parts**: Extra dest parts and their gaps are deleted (unless `keep_deleted_sections=True`)
- **Source has more parts**: Extra source parts are appended with their gaps

<!-- === DO_NOT_EDIT: pkg-ext replace_sections_changes === -->
### Changes

| Version | Change |
|---------|--------|
| 0.101.3 | added optional param 'keep_deleted_sections' (default: False) |
| 0.101.0 | Made public |
<!-- === OK_EDIT: pkg-ext replace_sections_changes === -->
