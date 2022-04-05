# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]
- nothing

## [1.1.2] - 2022-04-05
### Added
- "publish: false" in a page can disable rendering of a page. Can also be used as a global toggle
- Collections: added ORDER_KEY and ORDER_REVERSE options. Can be used to configure the order of posts within collection pages.

## [1.1.0] - 2022-04-03
### Added
- Collections: the OVERVIEW_CONTENT field allows to specify a markdown file to be used for the Collection overview page's content

### Fixed
- no longer ignores "meta" fields already set on a page. Previously they were overridden in the meta parsing process
- Collections: if a page belonging to a collection was not modified after a rebuild, it would not be passed through the plugin pipeline. Among other side effects, this did not allow for Timestamp- and ReadingTime-integration for post previews
- Timestamp: no longer panics if a file vanishes
- ToC: indented ToC HTML was not accessibility friendly

### Changed
- ReadingTime: if the plugin was configured with WPM_FAST and WPM_SLOW values being identical, or if the text was very short, the fast and slow estimate could be identical. In this case, the plugin now simply shows "0" instead of "0 - 0" (for example)
- the "content_raw" field utilized by some plugins now only contains the unparsed markdown content, where previously it also included the yaml headers

## [1.0.5] - 2022-02-23
### Fixed
- autoSEO: fixed double "/" issue in image URLs

### Changed
- silently ignores FileNotFound errors instead of throwing an exception, since usually, a temp file is at fault

## [1.0.4] - 2021-09-06
### Added
- "--desktop" flag for lighthouse (default is mobile)

### Fixed
- autoSEO: no longer crashes when no image can be found; ignores modular subpages
- pixelizer: save original image without blowing up its size
- minify: configuring minify no longer disables it
- toc: don't generate tocs for modular subpages
- highlight: regex non-greedy, previously wrong behaviour when multiple code blocks on a page; eliminated duplicate stylesheet generation

### Changed
- enabled git plugin by default
- higher resilience against errors (non-critical errors get logged instead of excepted)
- autoSEO: use site_name as fallback for title
- highlight: accepts more conventional / markdown-style lexer notation; un-escape code before highlighting
- collections: category & overview pages now passed through enabled plugins; use summary as preview, if it exists; preview-image does no longer have to be in the same directory

## [1.0.3] - 2021-09-01
### Fixed
- faulty system blueprints path made barely unable to find any blueprints

### Changed
- to ensure at least somewhat "unique" alt-tags in galleries, include the number-position of the image in the gallery
- original/fallback images will no longer be processed by PIL in the Pixelizer plugin, but rather just be copied; their filesizes got blown up before, and the step was needless anyways

## [1.0.2] - 2021-08-27
### Changed
- clean up raw_content before AutoSummary consumes it

### Fixed
- robots.txt no longer weirdly indented
- sitemap generation now works after fixing a typo (hmtl -> html)

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

[Unreleased]: https://github.com/charludo/barely/compare/v1.1.2...HEAD
[1.1.2]: https://github.com/charludo/barely/compare/v1.1.0...v1.1.2
[1.1.0]: https://github.com/charludo/barely/compare/v1.0.5...v1.1.0
[1.0.5]: https://github.com/charludo/barely/compare/v1.0.4...v1.0.5
[1.0.4]: https://github.com/charludo/barely/compare/v1.0.3...v1.0.4
[1.0.3]: https://github.com/charludo/barely/compare/v1.0.2...v1.0.3
[1.0.2]: https://github.com/charludo/barely/compare/v1.0.0...v1.0.2
[1.0.0]: https://github.com/charludo/barely/compare/v_095...v1.0.0
[0.9.5]: https://github.com/charludo/barely/compare/v_090...v_095
[0.9.0]: https://github.com/charludo/barely/releases/tag/v_090
