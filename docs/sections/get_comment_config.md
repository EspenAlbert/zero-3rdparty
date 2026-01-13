# get_comment_config

<!-- === DO_NOT_EDIT: pkg-ext get_comment_config_def === -->
## function: get_comment_config
- [source](../../_internal/sections.py#L81)

```python
def get_comment_config(path: Path | str, override: CommentConfig | None = None) -> CommentConfig:
    ...
```

The type of the None singleton.
<!-- === OK_EDIT: pkg-ext get_comment_config_def === -->

<!-- === DO_NOT_EDIT: pkg-ext get_comment_config_example_justfile_by_name === -->
### Example: justfile_by_name

```python
result = get_comment_config(path='justfile', override=None)
```
<!-- === OK_EDIT: pkg-ext get_comment_config_example_justfile_by_name === -->

<!-- === DO_NOT_EDIT: pkg-ext get_comment_config_example_markdown_file === -->
### Example: markdown_file

```python
result = get_comment_config(path=PosixPath('test.md'), override=None, expected_prefix='<!--', expected_suffix=' -->')
```
<!-- === OK_EDIT: pkg-ext get_comment_config_example_markdown_file === -->

<!-- === DO_NOT_EDIT: pkg-ext get_comment_config_example_python_file === -->
### Example: python_file

```python
result = get_comment_config(path=PosixPath('test.py'), override=None, expected_prefix='#', expected_suffix='')
```
<!-- === OK_EDIT: pkg-ext get_comment_config_example_python_file === -->

<!-- === DO_NOT_EDIT: pkg-ext get_comment_config_example_typescript_file === -->
### Example: typescript_file

```python
result = get_comment_config(path=PosixPath('app.ts'), override=None)
```
<!-- === OK_EDIT: pkg-ext get_comment_config_example_typescript_file === -->

<!-- === DO_NOT_EDIT: pkg-ext get_comment_config_example_with_override === -->
### Example: with_override

```python
result = get_comment_config(path=PosixPath('test.py'), override={'prefix': '%%', 'suffix': ''}, expected_prefix='%%', expected_suffix='')
```
<!-- === OK_EDIT: pkg-ext get_comment_config_example_with_override === -->

<!-- === DO_NOT_EDIT: pkg-ext get_comment_config_changes === -->
### Changes

| Version | Change |
|---------|--------|
| unreleased | Made public |
<!-- === OK_EDIT: pkg-ext get_comment_config_changes === -->