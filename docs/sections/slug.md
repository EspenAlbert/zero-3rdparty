# slug

<!-- === DO_NOT_EDIT: pkg-ext slug_def === -->
## function: slug
- [source](../../_internal/sections.py#L8)

```python
def slug(text: str) -> str:
    ...
```

The type of the None singleton.
<!-- === OK_EDIT: pkg-ext slug_def === -->

<!-- === DO_NOT_EDIT: pkg-ext slug_example_lowercase_pascal === -->
### Example: lowercase_pascal

```python
result = slug(text='HelloWorld')
```
<!-- === OK_EDIT: pkg-ext slug_example_lowercase_pascal === -->

<!-- === DO_NOT_EDIT: pkg-ext slug_example_preserve_underscores === -->
### Example: preserve_underscores

```python
result = slug(text='parse_config')
```
<!-- === OK_EDIT: pkg-ext slug_example_preserve_underscores === -->

<!-- === DO_NOT_EDIT: pkg-ext slug_example_spaces_to_underscores === -->
### Example: spaces_to_underscores

```python
result = slug(text='hello world')
```
<!-- === OK_EDIT: pkg-ext slug_example_spaces_to_underscores === -->

<!-- === DO_NOT_EDIT: pkg-ext slug_example_strip_special_chars === -->
### Example: strip_special_chars

```python
result = slug(text='Some.Thing!')
```
<!-- === OK_EDIT: pkg-ext slug_example_strip_special_chars === -->

<!-- === DO_NOT_EDIT: pkg-ext slug_changes === -->
### Changes

| Version | Change |
|---------|--------|
| unreleased | Made public |
<!-- === OK_EDIT: pkg-ext slug_changes === -->