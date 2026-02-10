<!-- === DO_NOT_EDIT: pkg-ext header === -->
# sections

<!-- === OK_EDIT: pkg-ext header === -->
<!-- === DO_NOT_EDIT: pkg-ext symbols === -->
- [`CommentConfig`](#commentconfig_def)
- [Section](./section.md)
- [`SectionChanges`](#sectionchanges_def)
- [SectionPart](./sectionpart.md)
- [`changed_sections`](#changed_sections_def)
- [`compare_sections`](#compare_sections_def)
- [`extract_sections`](#extract_sections_def)
- [`extract_sections_from_path`](#extract_sections_from_path_def)
- [`get_comment_config`](#get_comment_config_def)
- [`has_sections`](#has_sections_def)
- [`has_sections_in_path`](#has_sections_in_path_def)
- [`parse_sections`](#parse_sections_def)
- [`parse_sections_from_path`](#parse_sections_from_path_def)
- [replace_sections](./replace_sections.md)
- [`slug`](#slug_def)
- [`wrap_in_default_section`](#wrap_in_default_section_def)
- [`wrap_section`](#wrap_section_def)
<!-- === OK_EDIT: pkg-ext symbols === -->
<!-- === DO_NOT_EDIT: pkg-ext symbol_details_header === -->
## Symbol Details
<!-- === OK_EDIT: pkg-ext symbol_details_header === -->
<!-- === DO_NOT_EDIT: pkg-ext commentconfig_def === -->
<a id="commentconfig_def"></a>

### class: `CommentConfig`
- [source](../../zero_3rdparty/_internal/sections.py#L18)
> **Since:** 0.101.0

```python
class CommentConfig:
    prefix: str
    suffix: str = ''
```

| Field | Type | Default | Since |
|---|---|---|---|
| prefix | `str` | - | 0.101.0 |
| suffix | `str` | `''` | 0.101.0 |
<!-- === OK_EDIT: pkg-ext commentconfig_def === -->
<!-- === DO_NOT_EDIT: pkg-ext compare_sections_def === -->
<a id="compare_sections_def"></a>

### function: `compare_sections`
- [source](../../zero_3rdparty/_internal/sections.py#L256)
> **Since:** 0.101.0

```python
def compare_sections(baseline_content: str, current_content: str, tool_name: str, config: CommentConfig, skip: set[str] | None = None, filename: str = '') -> list[str]:
    ...
```

Return section IDs with changes (modified or removed), excluding skipped sections.
<!-- === OK_EDIT: pkg-ext compare_sections_def === -->
<!-- === DO_NOT_EDIT: pkg-ext extract_sections_def === -->
<a id="extract_sections_def"></a>

### function: `extract_sections`
- [source](../../zero_3rdparty/_internal/sections.py#L247)
> **Since:** 0.101.0

```python
def extract_sections(content: str, tool_name: str, config: CommentConfig, filename: str = '') -> dict[str, str]:
    ...
```
<!-- === OK_EDIT: pkg-ext extract_sections_def === -->
<!-- === DO_NOT_EDIT: pkg-ext extract_sections_from_path_def === -->
<a id="extract_sections_from_path_def"></a>

### function: `extract_sections_from_path`
- [source](../../zero_3rdparty/_internal/sections.py#L439)
> **Since:** 0.101.0

```python
def extract_sections_from_path(path: Path, tool_name: str) -> dict[str, str]:
    ...
```
<!-- === OK_EDIT: pkg-ext extract_sections_from_path_def === -->
<!-- === DO_NOT_EDIT: pkg-ext has_sections_def === -->
<a id="has_sections_def"></a>

### function: `has_sections`
- [source](../../zero_3rdparty/_internal/sections.py#L243)
> **Since:** 0.101.0

```python
def has_sections(content: str, tool_name: str, config: CommentConfig) -> bool:
    ...
```
<!-- === OK_EDIT: pkg-ext has_sections_def === -->
<!-- === DO_NOT_EDIT: pkg-ext has_sections_in_path_def === -->
<a id="has_sections_in_path_def"></a>

### function: `has_sections_in_path`
- [source](../../zero_3rdparty/_internal/sections.py#L434)
> **Since:** 0.101.0

```python
def has_sections_in_path(path: Path, tool_name: str) -> bool:
    ...
```
<!-- === OK_EDIT: pkg-ext has_sections_in_path_def === -->
<!-- === DO_NOT_EDIT: pkg-ext parse_sections_from_path_def === -->
<a id="parse_sections_from_path_def"></a>

### function: `parse_sections_from_path`
- [source](../../zero_3rdparty/_internal/sections.py#L429)
> **Since:** 0.101.0

```python
def parse_sections_from_path(path: Path, tool_name: str) -> list[Section]:
    ...
```
<!-- === OK_EDIT: pkg-ext parse_sections_from_path_def === -->
<!-- === DO_NOT_EDIT: pkg-ext slug_def === -->
<a id="slug_def"></a>

### function: `slug`
- [source](../../zero_3rdparty/_internal/sections.py#L12)
> **Since:** 0.101.0

```python
def slug(text: str) -> str:
    ...
```

Convert text to lowercase slug suitable for section marker IDs.
<!-- === OK_EDIT: pkg-ext slug_def === -->
<!-- === DO_NOT_EDIT: pkg-ext wrap_in_default_section_def === -->
<a id="wrap_in_default_section_def"></a>

### function: `wrap_in_default_section`
- [source](../../zero_3rdparty/_internal/sections.py#L304)
> **Since:** 0.101.0

```python
def wrap_in_default_section(content: str, tool_name: str, config: CommentConfig) -> str:
    ...
```
<!-- === OK_EDIT: pkg-ext wrap_in_default_section_def === -->
<!-- === DO_NOT_EDIT: pkg-ext wrap_section_def === -->
<a id="wrap_section_def"></a>

### function: `wrap_section`
- [source](../../zero_3rdparty/_internal/sections.py#L298)
> **Since:** 0.101.0

```python
def wrap_section(content: str, section_id: str, tool_name: str, config: CommentConfig) -> str:
    ...
```
<!-- === OK_EDIT: pkg-ext wrap_section_def === -->
<!-- === DO_NOT_EDIT: pkg-ext sectionchanges_def === -->
<a id="sectionchanges_def"></a>

### class: `SectionChanges`
- [source](../../zero_3rdparty/_internal/sections.py#L52)
> **Since:** 0.102.0

```python
class SectionChanges:
    modified: list[str]
    missing: list[str]
```

| Field | Type | Default | Since |
|---|---|---|---|
| modified | `list[str]` | - | 0.102.0 |
| missing | `list[str]` | - | 0.102.0 |
<!-- === OK_EDIT: pkg-ext sectionchanges_def === -->
<!-- === DO_NOT_EDIT: pkg-ext changed_sections_def === -->
<a id="changed_sections_def"></a>

### function: `changed_sections`
- [source](../../zero_3rdparty/_internal/sections.py#L275)
> **Since:** 0.102.0

```python
def changed_sections(baseline_content: str, current_content: str, tool_name: str, config: CommentConfig, skip: set[str] | None = None, filename: str = '') -> SectionChanges:
    ...
```

Return modified and missing sections separately.
<!-- === OK_EDIT: pkg-ext changed_sections_def === -->
<!-- === DO_NOT_EDIT: pkg-ext get_comment_config_def === -->
<a id="get_comment_config_def"></a>

### function: `get_comment_config`
- [source](../../zero_3rdparty/_internal/sections.py#L120)
> **Since:** 0.101.0

```python
def get_comment_config(path: Path | str, override: CommentConfig | None = None) -> CommentConfig:
    ...
```
<!-- === OK_EDIT: pkg-ext get_comment_config_def === -->
<!-- === DO_NOT_EDIT: pkg-ext parse_sections_def === -->
<a id="parse_sections_def"></a>

### function: `parse_sections`
- [source](../../zero_3rdparty/_internal/sections.py#L155)
> **Since:** 0.101.0

```python
def parse_sections(content: str, tool_name: str, config: CommentConfig, filename: str = '') -> list[Section]:
    ...
```
<!-- === OK_EDIT: pkg-ext parse_sections_def === -->