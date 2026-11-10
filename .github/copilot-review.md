# Code Review — Mopidy-Podcast 4.0.0

**Date:** 2026-11-10
**Reviewed:** `develop`, i.e. `master` at `95cd796` ("Bump codecov/codecov-action from
7.0.0 to 7.1.1", v4.0.0 plus dependency bumps) plus the build environment update, the
`lookup()`, feed error and test fixture fixes, "Exclude AGENTS.md from source
distributions.", "Add system site packages setting as comment to tox.ini." and this
review commit; `__version__` 4.0.0.

**CI status:** All default `tox` environments pass locally on CPython 3.13.18 (`py`:
36 passed) with Mopidy 4.0.5, cachetools 8.0.0, uritools 7.0.0 and Pykka 4.5.0; not
run on 3.14 locally. GitHub Actions is green on 3.13 and 3.14 for `develop` before
this review commit. `tox -e pyright` fails with 48 errors (Code #1). **Coverage:** 88
% with branches; gaps in `library.py` (80 %: config dir errors, `root_directory`
fallbacks) and `feeds.py` (89 %).

## Code — Potential Issues

| # | Priority | Location | Finding |
|---|----------|----------|---------|
| 1 | Low | whole package, `tests/` | pyright `standard` reports 48 errors: Mopidy 4's typed models (`Uri`, `ReleaseDate`, `DurationMs`, `frozenset` artists, `tuple` results) reject plain `str`, `int` and `list` arguments, `self.backend.feeds` is unknown on `backend.Backend`, and the `root_directory` property overrides a class attribute. Blocks adding `pyright` to the envlist. |
| 2 | Info | `library.py` `get_images` | `get_images(None)` raises `TypeError` instead of returning `{}`, unlike the other provider methods (asserted by `test_get_images_error`). |

## Tests — Gaps

| # | Priority | Finding |
|---|----------|---------|
| 1 | Low | `PodcastFeedCache.__missing__` is only exercised with `file:` URIs; the path that stores remote feeds (line 35) and the TTL/size limits from the config are untested, as is the HTTP opener's timeout. |
| 2 | Low | `root_directory` is tested only for a relative `browse_root`; absolute paths, URLs, an empty setting and an unavailable config directory (`get_config_dir` errors) are not. |
| 3 | Info | `itunes:duration` values with hours or only seconds, missing or malformed `pubDate`, and items without `<guid>` but with an enclosure are covered only partly by `tests/rssfeed.xml`. |
| 4 | Info | Two `DeprecationWarning`s ("Use ReleaseDate instead") come from `mopidy.types` at import time, not from this package. |

## Changelog

| # | Priority | Finding |
|---|----------|---------|
| 1 | Medium | The next release's entry needs "Fix ``lookup()`` returning ``None`` for an unknown episode guid." and "Improve error handling for invalid feeds.", plus "Update build environment." for the ruff, `tox` and CI changes and one "Minor test improvements." line for the `conftest.py` fix. |
