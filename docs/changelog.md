# Change Log

This page tracks notable changes to the LanguageCheck API and documentation.

An [RSS feed](/changelog/feed.xml) of these releases is updated on each documentation build.

## Unreleased

- No changes yet.

## 2.2.0 - 2026-11-26

### Added

- `POST /file-check` to start a language check from bilingual files. Send one HTTP(S) URL in `fileUrl`, several URLs in `fileUrls` (no zip), or one or more `file` parts in `multipart/form-data`.
- `GET /file-check/{processId}` for progress, `PUT /file-check/{processId}` to start a process left in `DRAFT` after `onlyImport`, and `DELETE /file-check/{processId}` to delete a process created through this API.
- File-check options `onlyImport`, `lcAsAuthor`, `markAsLocked`, `webhookUrl`, and email `notifications` (`onStart`, `onError`, `onComplete`).
- Rate limits for the file-check operations: 20 requests/minute and 2 requests/second for create, start, and delete; 60 requests/minute and 10 requests/second for progress.

### Changed

- Burst limit for `GET /status` and `GET /wallet` is 5 requests/second.
- `shortSegmentsMaxSourceWords` turns short-segment handling on only when the field is present and greater than 0.

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
