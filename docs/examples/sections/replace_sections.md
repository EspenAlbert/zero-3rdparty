<!--
description: Replace managed section content while preserving user-editable gaps
-->
# replace_sections

Replaces section content in a destination string using source sections, preserving preamble and inter-section content.

## Basic Replacement

```python
from zero_3rdparty.sections import CommentConfig, replace_sections

dest = """\
preamble
# === DO_NOT_EDIT: tool header ===
old content
# === OK_EDIT: tool header ===
"""
result = replace_sections(dest, {"header": "new content"}, "tool", CommentConfig("#"))
print(result)
"""
preamble
# === DO_NOT_EDIT: tool header ===
new content
# === OK_EDIT: tool header ===
"""
```

## Keep Deleted Sections

When a source section is missing, `keep_deleted_sections=True` preserves the destination section:

```python
from zero_3rdparty.sections import CommentConfig, replace_sections

dest = """\
# === DO_NOT_EDIT: tool a ===
content a
# === OK_EDIT: tool a ===
# === DO_NOT_EDIT: tool b ===
content b
# === OK_EDIT: tool b ===
"""
result = replace_sections(dest, {"a": "updated a"}, "tool", CommentConfig("#"), keep_deleted_sections=True)
print(result)
"""
# === DO_NOT_EDIT: tool a ===
updated a
# === OK_EDIT: tool a ===
# === DO_NOT_EDIT: tool b ===
content b
# === OK_EDIT: tool b ===
"""
```

## Skip Sections

Use `skip_sections` to leave specific sections untouched:

```python
from zero_3rdparty.sections import CommentConfig, replace_sections

dest = """\
# === DO_NOT_EDIT: tool x ===
keep me
# === OK_EDIT: tool x ===
# === DO_NOT_EDIT: tool y ===
replace me
# === OK_EDIT: tool y ===
"""
result = replace_sections(dest, {"x": "ignored", "y": "new y"}, "tool", CommentConfig("#"), skip_sections=["x"])
print(result)
"""
# === DO_NOT_EDIT: tool x ===
keep me
# === OK_EDIT: tool x ===
# === DO_NOT_EDIT: tool y ===
new y
# === OK_EDIT: tool y ===
"""
```
