<!--
description: Frozen dataclass holding comment prefix/suffix for section markers
-->
# CommentConfig

`CommentConfig(prefix, suffix='')` defines how section markers are delimited. The `prefix` opens a comment and the optional `suffix` closes it.

## Hash Comments (Python, YAML, shell)

```python
from zero_3rdparty.sections import CommentConfig, wrap_in_default_section

cfg = CommentConfig("#")
print(cfg)
#> CommentConfig(prefix='#', suffix='')

print(wrap_in_default_section("managed content", "tool", cfg))
"""
# === DO_NOT_EDIT: tool default ===
managed content
# === OK_EDIT: tool default ===
"""
```

## HTML Comments (Markdown, HTML, XML)

```python
from zero_3rdparty.sections import CommentConfig, wrap_in_default_section

cfg = CommentConfig("<!--", " -->")
print(cfg)
#> CommentConfig(prefix='<!--', suffix=' -->')

print(wrap_in_default_section("# Title", "pkg", cfg))
"""
<!-- === DO_NOT_EDIT: pkg default === -->
# Title
<!-- === OK_EDIT: pkg default === -->
"""
```

## Parsing with Different Configs

The same `parse_sections` call works with any config - only the marker format changes:

```python
from zero_3rdparty.sections import CommentConfig, parse_sections

html_content = """\
<!-- === DO_NOT_EDIT: pkg heading === -->
# Title
<!-- === OK_EDIT: pkg heading === -->
"""
sections = parse_sections(html_content, "pkg", CommentConfig("<!--", " -->"))
print(sections[0].id)
#> heading
print(sections[0].content)
#> # Title
```

## Extension Map

`EXTENSION_COMMENT_MAP` maps file extensions to their `CommentConfig`:

```python
from zero_3rdparty._internal.sections import EXTENSION_COMMENT_MAP

print(EXTENSION_COMMENT_MAP[".py"])
#> CommentConfig(prefix='#', suffix='')

print(EXTENSION_COMMENT_MAP[".md"])
#> CommentConfig(prefix='<!--', suffix=' -->')

print(EXTENSION_COMMENT_MAP[".js"])
#> CommentConfig(prefix='//', suffix='')

print(EXTENSION_COMMENT_MAP[".css"])
#> CommentConfig(prefix='/*', suffix=' */')
```

## Filename Map

Files without extensions (e.g. `justfile`, `Makefile`) are handled by `FILENAME_COMMENT_MAP`:

```python
from zero_3rdparty._internal.sections import FILENAME_COMMENT_MAP

print(FILENAME_COMMENT_MAP["justfile"])
#> CommentConfig(prefix='#', suffix='')

print(FILENAME_COMMENT_MAP["Dockerfile"])
#> CommentConfig(prefix='#', suffix='')

print("Makefile" in FILENAME_COMMENT_MAP)
#> True
```
