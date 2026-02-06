# SectionPart

<!-- === DO_NOT_EDIT: pkg-ext sectionpart_def === -->
## class: SectionPart
- [source](../../zero_3rdparty/_internal/sections.py#L24)
> **Since:** 0.103.0

```python
class SectionPart:
    content: str
    start_line: int
    end_line: int
    content_after: str | None = None
```
<!-- === OK_EDIT: pkg-ext sectionpart_def === -->

### Fields

| Field | Type | Default | Since |
|---|---|---|---|
| content | `str` | - | 0.103.0 |
| start_line | `int` | - | 0.103.0 |
| end_line | `int` | - | 0.103.0 |
| content_after | `str | None` | `None` | 0.104.0 |

<!-- === DO_NOT_EDIT: pkg-ext sectionpart_changes === -->
### Changes

| Version | Change |
|---------|--------|
| 0.104.0 | field 'content_after' default: '' -> None |
| 0.104.0 | field 'content_after' type: str -> str | None |
| 0.103.0 | Made public |
<!-- === OK_EDIT: pkg-ext sectionpart_changes === -->