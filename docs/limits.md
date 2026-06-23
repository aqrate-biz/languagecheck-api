# Limits

Rate limits protect platform stability and ensure fair usage.

Unless otherwise agreed, limits are enforced per account linked to the API key.

## Endpoint Rate Limits

| Endpoint  |     Sustained limit |       Burst limit |
| --------- | ------------------: | ----------------: |
| `/check`  | 100 requests/minute | 5 requests/second |
| `/status` |   5 requests/minute |  1 request/second |
| `/wallet` |   5 requests/minute |  1 request/second |

Both limits apply: a request can be rejected if either the per-minute or per-second threshold is exceeded.

## When You Hit a Limit

If your client exceeds a limit, the API returns a rate-limit error (typically HTTP 429).

Recommended client behavior:

- Retry with exponential backoff and jitter.
- Reduce concurrency and request bursts.
- Respect `Retry-After` when present.

## Word Balance and Quota

Use `/wallet` to inspect the number of words still available for the authenticated user. This helps you display remaining quota, pause or defer `/check` requests when the balance is low, and avoid unexpected failures on exhausted usage plans.

## Implementation Guidance

- Implement client-side throttling for both per-second and per-minute windows.
- Keep `/status` polling minimal; avoid aggressive health-check loops.
- Queue `/check` traffic and drain at a controlled rate.
- Monitor rate-limit responses and alert on repeated throttling.
- Call `/wallet` sparingly for pre-flight checks rather than in tight polling loops.

## Need Higher Throughput?

Contact support with your expected request profile (average RPM, peak RPS, and use case).
