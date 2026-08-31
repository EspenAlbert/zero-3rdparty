<!--
description: Parse content with DO_NOT_EDIT/OK_EDIT markers into Section objects
-->
# parse_sections

Parses content containing `DO_NOT_EDIT`/`OK_EDIT` markers into a list of `Section` objects.

## Basic Usage

```python
from zero_3rdparty.sections import CommentConfig, parse_sections

content = """\
# === DO_NOT_EDIT: tool header ===
managed line 1
managed line 2
# === OK_EDIT: tool header ===
"""
sections = parse_sections(content, "tool", CommentConfig("#"))
print(sections[0].id)
# > header
print(sections[0].content)
"""
managed line 1
managed line 2
"""
```

## Multiple Sections

```python
from zero_3rdparty.sections import CommentConfig, parse_sections

content = """\
# === DO_NOT_EDIT: tool alpha ===
first
# === OK_EDIT: tool alpha ===
# === DO_NOT_EDIT: tool beta ===
second
# === OK_EDIT: tool beta ===
"""
sections = parse_sections(content, "tool", CommentConfig("#"))
print([s.id for s in sections])
# > ['alpha', 'beta']
```

## Multi-part Sections (Resumable)

A section can pause and resume, creating multiple parts:

```python
from zero_3rdparty.sections import CommentConfig, parse_sections

content = """\
# === DO_NOT_EDIT: tool job ===
part 1
# === OK_EDIT: tool job ===
user content here
# === DO_NOT_EDIT: tool job ===
part 2
# === OK_EDIT: tool job ===
"""
sections = parse_sections(content, "tool", CommentConfig("#"))
print(len(sections[0].parts))
# > 2
print(sections[0].parts[0].content)
# > part 1
print(sections[0].parts[1].content)
# > part 2
```
