<!--
description: Frozen dataclass holding comment prefix/suffix for section markers
-->
# CommentConfig

`CommentConfig` defines how section markers are commented in different file types.

## Creating Configs

```python
from zero_3rdparty.sections import CommentConfig

py_config = CommentConfig(prefix="#")
print(py_config)
#> CommentConfig(prefix='#', suffix='')

html_config = CommentConfig("<!--", " -->")
print(html_config)
#> CommentConfig(prefix='<!--', suffix=' -->')
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
