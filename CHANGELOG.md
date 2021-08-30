# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
### Changed
- to ensure at least somewhat "unique" alt-tags in galleries, include the number-position of the image in the gallery
- original/fallback images will no longer be processed by PIL in the Pixelizer plugin, but rather just be copied; their filesizes got blown up before, and the step was needless anyways

## [1.0.0] - 2021-08-26
### Added
- lighthouse CLI integration
- AutoSEO plugin
- AutoSummary plugin
- Gallery plugin
- Minify plugin
- Pixelizer plugin
- global `-d` debugging-flag
- this changelog!

### Changed
- moved from BETA to STABLE
- switched version numbering scheme from `v_095` to more readable `v1.0.0`
- proper logging instead of print()
- simplified the default blueprint to make it more usable

### Fixed
- various small performance improvements, largely due to eliminating duplicate function calls

### Removed
- Minimizer plugin, obsolete thanks to Minify and Pixelizer

## [0.9.5] - 2021-07-19
### Added
- `-l` flag for light rebuilds (no re-rendering of images, preserves webroot)
- `-s` flag to start the live server after a rebuild

### Fixed
- bugs preventing forms and collections from being compiled correctly
- unability to render an item no longer crashes barely

## [0.9.0] - 2021-06-19
Initial beta release

[Unreleased]: https://github.com/charludo/barely/compare/v1.0.0...HEAD
[1.0.0]: https://github.com/charludo/barely/compare/v_095...v1.0.0
[0.9.5]: https://github.com/charludo/barely/compare/v_090...v_095
[0.9.0]: https://github.com/charludo/barely/releases/tag/v_090
