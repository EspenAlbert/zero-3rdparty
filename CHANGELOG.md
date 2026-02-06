# Changelog

## 0.104.0 2026-02-06T06-59Z

### Sections
- BREAKING `sections.SectionPart`: field 'content_after' type: str -> str | None
- BREAKING `sections.Section`: field 'content_after' type: str -> str | None
- fix(sections): preserve single blank lines between sections [ae5365](https://github.com/EspenAlbert/zero-3rdparty/commit/ae5365)
- `sections.SectionPart`: field 'content_after' default: '' -> None
- `sections.Section`: field 'content_after' default: '' -> None


## 0.103.0 2026-02-06T05-56Z

### Sections
- BREAKING `sections.Section`: removed field 'end_line'
- BREAKING `sections.Section`: removed field 'content'
- BREAKING `sections.Section`: removed field 'start_line'
- BREAKING `sections.replace_sections`: param 'src_sections' type: dict[str, str] -> dict[str, str] | list[Section]
- New class `SectionPart`
- `sections.Section`: added optional field 'parts' (default: ...)
- `sections.Section`: added optional field 'content_after' (default: '')


## 0.102.0 2026-01-24T19-19Z

### Sections
- New function `changed_sections`
- New class `SectionChanges`
- fix: replace_sections empty content should also write end marker [637c17](https://github.com/EspenAlbert/zero-3rdparty/commit/637c17)
- fix: Enhances section parsing for hyphenated IDs [a557d4](https://github.com/EspenAlbert/zero-3rdparty/commit/a557d4)


## 0.101.3 2026-01-19T07-29Z

### Sections
- fix: update section replacement logic to delete dest-only sections by default, with options to preserve them using skip_sections or keep_deleted_sections [6fd5b2](https://github.com/EspenAlbert/zero-3rdparty/commit/6fd5b2)
- `sections.replace_sections`: added optional param 'keep_deleted_sections' (default: False)


## 0.101.1 2026-01-14T14-41Z

### Sections
- fix: enhance section parsing functions to include filename in error messages and add support for additional file types [ec3be0](https://github.com/EspenAlbert/zero-3rdparty/commit/ec3be0)


## 0.101.0 2026-01-13T21-37Z

### Sections
- New function slug
- New function get_comment_config
- New function parse_sections
- New function has_sections
- New function extract_sections
- New function compare_sections
- New function wrap_section
- New function wrap_in_default_section
- New function replace_sections
- New function parse_sections_from_path
- New function has_sections_in_path
- New function extract_sections_from_path
- New class CommentConfig
- New class Section
