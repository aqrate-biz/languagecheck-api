# LanguageCheck API

**Version:** 2.0.1  
**Base URL:** `https://apitest.languagecheck.it/v2`

---

## Overview

The LanguageCheck API provides programmatic access to the services offered by [languagecheck.ai](https://languagecheck.ai). It exposes a RESTful interface over HTTPS and is designed for integration into translation workflows, quality assurance pipelines, and any application that needs automated assessment of bilingual content.

---

## Endpoints

### GET /status — Service Health Check

This endpoint returns the current operational status of the LanguageCheck service and its underlying AI infrastructure. It accepts no parameters.

The response indicates whether the platform and the AI service are fully operational, experiencing degraded performance, or undergoing maintenance. It is useful for health checks in monitoring dashboards, or for verifying service availability before submitting translation segments.

---

### POST /check — Translation Quality Evaluation

This is the primary endpoint of the API. It accepts a bilingual segment — a source text and its corresponding translation — along with the respective language codes, and returns a structured evaluation of the translation quality.

The evaluation covers three dimensions: **major errors** (issues that distort meaning or render the translation unsuitable), **minor errors** (inaccuracies or stylistic imprecisions that do not significantly affect usability), and **fluency issues** (problems with the naturalness and readability of the target text, independently of its accuracy). Each dimension is accompanied by a textual explanation when issues are detected.

The response also includes an **overall verdict** for the segment and an **ambiguity flag**, which signals that the model could not assess the segment with sufficient confidence — typically due to very short or highly technical content — and that human review may be warranted.

Explanations can be returned in a configurable language, making it straightforward to surface QA feedback directly to translators or reviewers in their preferred language.
