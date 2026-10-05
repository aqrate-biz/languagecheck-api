# LanguageCheck API

**Version:** 2.1.0
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
