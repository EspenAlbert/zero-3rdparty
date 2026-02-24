<!--
description: Resolve CommentConfig from a file path or override
-->
# get_comment_config

Resolves the `CommentConfig` for a file path by extension or filename lookup.

## Basic Resolution

```python
from zero_3rdparty.sections import get_comment_config

py_config = get_comment_config("src/main.py")
print(py_config.prefix)
#> #

md_config = get_comment_config("docs/readme.md")
print(f"{md_config.prefix!r} {md_config.suffix!r}")
#> '<!--' ' -->'
```

## Override Takes Precedence

```python
from zero_3rdparty.sections import CommentConfig, get_comment_config

custom = CommentConfig("//")
result = get_comment_config("file.py", override=custom)
print(result.prefix)
#> //
```

## Unknown Extension Raises ValueError

```python
from zero_3rdparty.sections import get_comment_config

try:
    get_comment_config("data.xyz")
except ValueError as e:
    print(e)
    #> No comment config for: data.xyz (extension='.xyz')
```
