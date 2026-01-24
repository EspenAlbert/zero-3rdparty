# get_comment_config

<!-- === DO_NOT_EDIT: pkg-ext get_comment_config_def === -->
## function: get_comment_config
- [source](../../zero_3rdparty/_internal/sections.py#L90)
> **Since:** 0.101.0

```python
def get_comment_config(path: Path | str, override: CommentConfig | None = None) -> CommentConfig:
    ...
```
<!-- === OK_EDIT: pkg-ext get_comment_config_def === -->

<!-- === DO_NOT_EDIT: pkg-ext get_comment_config_example_markdown_file === -->
### Example: markdown_file

```python
result = get_comment_config(path=PosixPath("test.md"), override=None)
```
<!-- === OK_EDIT: pkg-ext get_comment_config_example_markdown_file === -->

<!-- === DO_NOT_EDIT: pkg-ext get_comment_config_example_python_file === -->
### Example: python_file

```python
result = get_comment_config(path=PosixPath("test.py"), override=None)
```
<!-- === OK_EDIT: pkg-ext get_comment_config_example_python_file === -->

<!-- === DO_NOT_EDIT: pkg-ext get_comment_config_example_with_override === -->
### Example: with_override

```python
result = get_comment_config(
    path=PosixPath("test.py"), override={"prefix": "%%", "suffix": ""}
)
```
<!-- === OK_EDIT: pkg-ext get_comment_config_example_with_override === -->

<!-- === DO_NOT_EDIT: pkg-ext get_comment_config_changes === -->
### Changes

| Version | Change |
|---------|--------|
| 0.101.0 | Made public |
<!-- === OK_EDIT: pkg-ext get_comment_config_changes === -->