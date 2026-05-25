# Usage

The LanguageCheck API is designed for synchronous validation of bilingual content and can be used in real-time or batch-oriented workflows.

## Common Use Cases

- Validate translated segments before publication.
- Enforce quality gates in localization pipelines.
- Assist reviewers with structured issue detection.
- Run automated checks during content ingestion.

## Integration Patterns

### Real-Time Validation

Use the API during authoring or review when users need immediate feedback.

### Batch Processing

Send queued segments from jobs, workers, or pipeline stages when throughput is more important than immediate response.

## Implementation Notes

- Respect request limits for your environment.
- Retry transient failures with backoff.
- Log request identifiers when available.
- Avoid sending unnecessary duplicate requests.
