# Limits

Rate limits protect platform stability and ensure fair usage.

Unless otherwise agreed, limits are enforced per account linked to the API key.

## Endpoint Rate Limits

| Endpoint                       |     Sustained limit |        Burst limit |
| ------------------------------ | ------------------: | -----------------: |
| `GET /status`                  |   5 requests/minute |  5 requests/second |
| `POST /check`                  | 100 requests/minute |  5 requests/second |
| `POST /multisegment-check`     | 100 requests/minute |  5 requests/second |
| `POST /multilanguage-check`    | 100 requests/minute |  5 requests/second |
| `POST /file-check`             |  20 requests/minute |  2 requests/second |
| `GET /file-check/{processId}`  |  60 requests/minute | 10 requests/second |
| `PUT /file-check/{processId}`  |  20 requests/minute |  2 requests/second |
| `DELETE /file-check/{processId}` | 20 requests/minute |  2 requests/second |
| `GET /wallet`                  |   5 requests/minute |  5 requests/second |

Both limits apply: a request can be rejected if either the per-minute or per-second threshold is exceeded.

## When You Hit a Limit

If your client exceeds a limit, the API returns a rate-limit error (typically HTTP 429).

Recommended client behavior:

- Retry with exponential backoff and jitter.
- Reduce concurrency and request bursts.
- Respect `Retry-After` when present.

## Word Balance and Quota

Use `/wallet` to inspect the number of words still available for the authenticated user. This helps you display remaining quota, pause or defer check requests when the balance is low, and avoid unexpected failures on exhausted usage plans.

## Implementation Guidance

- Implement client-side throttling for both per-second and per-minute windows.
- Keep `GET /status` and `GET /wallet` within 5 requests/minute and 5 requests/second.
- Queue `POST /check`, `POST /multisegment-check`, and `POST /multilanguage-check` at up to 100 requests/minute and 5 requests/second.
- Keep file-check create, start, and delete calls within 20 requests/minute and 2 requests/second. Progress polling on `GET /file-check/{processId}` allows 60 requests/minute and 10 requests/second.
- Monitor rate-limit responses and alert on repeated throttling.

## Need Higher Throughput?

Contact support at crew@languagecheck.ai with your expected request profile (average RPM, peak RPS, and use case).
