# Changelog

## [0.1.0] - 2026-06-24

### Added

- Initial public release
- Core audio chaptering library
- Reference implementations for analysis, cutting, and writing
- Command-line interface


## [0.2.0] - 2026-10-04

### Added

#### General
- CLFv1 format specification

#### CLI
- support for splitting audio according to chapter definitions
  provided in a CLF file
- `--clf` option to the `split` command

#### Library
- `ChapterEntry` and `ChapterList` domain models
- `ClfParser`
- `ChapterListAnalyzer`

### Changed

#### Library
- **BREAKING:** `Chapter.metadata` type: `dict[str, object]` → `frozendict[str, str]`

### Removed

#### Library
- **BREAKING:** `Domain Model Error` exception hierarchy (`InvalidChapterError`). Invalid domain models now raise `ValueError`.
