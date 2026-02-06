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
| unreleased | added optional field 'content_after' (default: '') |
| unreleased | added optional field 'parts' (default: ...) |
| unreleased | removed field 'start_line' |
| unreleased | removed field 'content' |
| unreleased | removed field 'end_line' |
| 0.101.0 | Made public |
<!-- === OK_EDIT: pkg-ext section_changes === -->