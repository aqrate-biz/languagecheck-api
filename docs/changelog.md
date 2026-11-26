# Change Log

This page tracks notable changes to the LanguageCheck API and documentation.

An [RSS feed](/changelog/feed.xml) of these releases is updated on each documentation build.

## Unreleased

- No changes yet.

## 2.1.1 - 2026-10-05

### Added

- `es-US` (Spanish, United States) to the supported language codes.

## 2.1.0 - 2026-09-21

### Added

- `GET /wallet` endpoint for the remaining word balance of the authenticated user.
- `POST /multisegment-check` endpoint to evaluate up to 10 bilingual segments in one request.

### Changed

- Sustained and burst limits for `/check` are 100 requests/minute and 5 requests/second.

## 2.0.0 - 2026-06-19

First public release of the LanguageCheck API.

### Added

- Initial `/check` endpoint for bilingual quality checks.
- `/status` endpoint for service availability checks.
- API key authentication.
- Developer documentation portal (getting started, authentication, API reference, limits, and support pages).

## Versioning Policy

Backward-compatible updates may be released without a major version change.

Breaking changes, if introduced, should be announced in advance together with migration guidance and rollout timing.
