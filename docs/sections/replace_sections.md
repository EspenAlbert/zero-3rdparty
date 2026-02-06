# replace_sections

<!-- === DO_NOT_EDIT: pkg-ext replace_sections_def === -->
## function: replace_sections
- [source](../../zero_3rdparty/_internal/sections.py#L326)
> **Since:** 0.101.0

```python
def replace_sections(dest_content: str, src_sections: dict[str, str] | list[Section], tool_name: str, config: CommentConfig, skip_sections: list[str] | None = None, *, keep_deleted_sections: bool = False) -> str:
    ...
```

Replace sections in dest_content with src_sections, preserving user content.
<!-- === OK_EDIT: pkg-ext replace_sections_def === -->

### Content Preservation

The function preserves three types of user content:

1. **Preamble**: Content before the first section marker
2. **Intra-section content** (`SectionPart.content_after`): Content between parts of a resumable section
3. **Inter-section content** (`Section.content_after`): Content between sections or after the last section

#### Intra-Section Content (Resumable Sections)

When a section has multiple parts (resumable sections), the function handles user content between parts:

- **Existing dest with content**: Dest content is preserved, source content is ignored
- **Empty dest content**: Source content is used as boilerplate template
- **New file (no dest sections)**: Source content is included as default
- **Source has fewer parts**: Extra dest parts are deleted (unless `keep_deleted_sections=True`)
- **Source has more parts**: Extra source parts are appended with their content

#### Inter-Section and Trailing Content

Content between different sections and content after the last section is preserved:

- **Dest has content**: Dest's inter-section/trailing content is preserved
- **New file**: Source's `Section.content_after` is used as template
- **Dest content cleared**: Empty content is preserved (source template not re-injected)

<!-- === DO_NOT_EDIT: pkg-ext replace_sections_changes === -->
### Changes

| Version | Change |
|---------|--------|
| 0.103.0 | param 'src_sections' type: dict[str, str] -> dict[str, str] | list[Section] |
| 0.101.3 | added optional param 'keep_deleted_sections' (default: False) |
| 0.101.0 | Made public |
<!-- === OK_EDIT: pkg-ext replace_sections_changes === -->