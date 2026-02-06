# Section

<!-- === DO_NOT_EDIT: pkg-ext section_def === -->
## class: Section
- [source](../../zero_3rdparty/_internal/sections.py#L32)
> **Since:** 0.101.0

```python
class Section:
    id: str
    parts: list[SectionPart] = ...
    content_after: str = ''
```
<!-- === OK_EDIT: pkg-ext section_def === -->

### Fields

| Field | Type | Default | Description |
|---|---|---|---|
| id | `str` | - | Section identifier from the marker |
| parts | `list[SectionPart]` | `[]` | Managed content parts (resumable sections have multiple) |
| content_after | `str` | `''` | User content after this section until next section or EOF |

<!-- === DO_NOT_EDIT: pkg-ext section_changes === -->
### Changes

| Version | Change |
|---------|--------|
| 0.103.0 | added optional field 'content_after' (default: '') |
| 0.103.0 | added optional field 'parts' (default: ...) |
| 0.103.0 | removed field 'start_line' |
| 0.103.0 | removed field 'content' |
| 0.103.0 | removed field 'end_line' |
| 0.101.0 | Made public |
<!-- === OK_EDIT: pkg-ext section_changes === -->