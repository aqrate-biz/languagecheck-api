# LanguageCheck API

**Version:** 2.1.1
**Base URL:** `https://api.languagecheck.ai/v2`

---

## Overview

The LanguageCheck API provides programmatic access to the services offered by [languagecheck.ai](https://languagecheck.ai). It exposes a RESTful interface over HTTPS and is designed for integration into translation workflows, quality assurance pipelines, and any application that needs automated assessment of bilingual content.

---

## Endpoints

### GET /status — Service Health Check

This endpoint returns the current operational status of the LanguageCheck service and its underlying AI infrastructure. It accepts no parameters.

The response indicates whether the platform and the AI service are fully operational, experiencing degraded performance, or undergoing maintenance. It is useful for health checks in monitoring dashboards, or for verifying service availability before submitting translation segments.

---

### GET /wallet — Remaining Words Balance

This endpoint returns the current number of words still available for the authenticated user. It is useful for checking quota before sending translation jobs and for surfacing remaining capacity in your application.

The response includes the remaining word count and the timestamp of the last wallet update, which can be used to keep UI indicators or internal monitoring in sync.

---

### POST /check — Translation Quality Evaluation

This is the primary endpoint of the API. It accepts a bilingual segment — a source text and its corresponding translation — along with the respective language codes, and returns a structured evaluation of the translation quality.

The evaluation covers three dimensions: **major errors** (issues that distort meaning or render the translation unsuitable), **minor errors** (inaccuracies or stylistic imprecisions that do not significantly affect usability), and **fluency issues** (problems with the naturalness and readability of the target text, independently of its accuracy). Each dimension is accompanied by a textual explanation when issues are detected.

The response also includes an **overall verdict** for the segment and an **ambiguity flag**, which signals that the model could not assess the segment with sufficient confidence and that human review may be needed.

Explanations can be returned in a configurable language, making it straightforward to surface QA feedback directly to translators or reviewers in their preferred language.

---

### POST /multisegment-check — Batch Translation Quality Evaluation

This endpoint evaluates multiple bilingual segments in a single request. It accepts between 1 and 10 segments, with shared source, target, and response languages. Each segment must have a unique `id` and contains its own source text and translation.

Segments are evaluated independently. The response contains one item per segment, in the same order as the request, and uses the supplied `id` to correlate each result with its input. A successful item contains the same structured quality evaluation returned by `POST /check`. If an individual segment is invalid or cannot be processed, only that item contains an error; the remaining valid segments can still complete successfully.

Request-level validation errors, such as missing shared languages, duplicate segment IDs, or more than 10 segments, reject the entire request. Before processing begins, the endpoint also checks that the wallet has enough words for all valid segments combined.

---

### POST /file-check — File Translation Quality Evaluation

This endpoint starts a language check from a bilingual file and returns a process id. Import and evaluation continue after the response, so use it to submit a file and then follow progress with `GET /file-check/{processId}` or a webhook.

Send the file in one of two ways. With `application/json`, set `fileUrl` to an HTTP(S) URL and the server downloads it (up to 100 MiB for a single bilingual file, up to 30 MiB for a zip). With `multipart/form-data`, send the bytes in the `file` part (up to 30 MiB) and the options in a `json` part with content type `application/json`. Accepted files are mqxliff, xlf, txlf, xliff, mxliff, sdlxliff. A zip of those files is expanded on the server; each entry can be up to 100 MiB, and nested zip files are skipped.

By default the language check starts as soon as the draft import finishes. When it completes, LanguageCheck writes an annotated XLIFF. Set `lcAsAuthor` to record LanguageCheck as the author of those edits, and `markAsLocked` to lock segments that have no issues. An optional `webhookUrl` is called when the check finishes, and also when import, start, or finalize fails. Webhook options can attach the annotated XLIFF, include signed URLs for the Excel report and the annotated files (valid up to 7 days), include segment and word counts by evaluation band, choose `POST` or `PUT`, and merge extra fields into the payload.

Set `onlyImport` to true to stop after the draft import. The process stays in `DRAFT`, and the webhook, when set, reports `success`, `processId`, `words`, and `error`. Words are debited when the check starts, so this pause is a way to confirm the word count against the wallet before evaluation. Start that process later with `PUT /file-check/{processId}`, or with another `POST /file-check` that sets both `action` and `processId` and omits the file. You can also pass a display name, the language of the explanations, translation context, and filters for locked segments, match percent, short segments, and target length.

---

### GET /file-check/{processId} — File Check Progress

This endpoint returns a progress snapshot for a file check. Poll it while the import or the evaluation is still running, and use it to drive a progress indicator next to the webhook.

The snapshot includes the process `status`, the time of the last progress update, how many segments have been processed, how many segments are expected, and the word count of the imported files. Progress counts can be null until check data exists. `words` is the sum of the word counts of the imported files.

---

### PUT /file-check/{processId} — Start an Imported File Check

This endpoint starts the language check for a process created with `POST /file-check` and `onlyImport` set to true. The body is `{ "action": "START" }`. The process must still be in `DRAFT`, and the check must not already have been started.

From that point the flow matches a file check submitted without `onlyImport`: the evaluation runs, the annotated XLIFF is written with the options stored when the process was created, and the webhook is called when the check ends. The same start can be requested with `POST /file-check` by setting both `action` and `processId`.

---

### DELETE /file-check/{processId} — Delete a File Check

This endpoint deletes the file check identified by `processId`. It accepts only processes created through `POST /file-check`. The response confirms that the deletion was accepted and includes the process id.
