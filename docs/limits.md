# Limits

API limits help protect service stability and ensure fair usage across tenants.

Exact quotas may vary by plan, environment, or commercial agreement.

## Limit Categories

- Request rate limits
- Payload size limits
- Concurrency limits
- Retention or history limits for related resources

## Best Practices

- Implement exponential backoff for retryable failures.
- Throttle burst traffic on the client side.
- Split very large workloads into smaller batches.
- Monitor error responses associated with quota exhaustion.

If you need higher throughput, contact support with your expected traffic profile and workload pattern.
