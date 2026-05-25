# Webhooks

LanguageCheck can notify your systems when asynchronous events are available.

If webhook delivery is enabled for your account, configure an HTTPS endpoint that can receive event payloads from LanguageCheck and return a successful status code after processing.

## Typical Flow

1. Register a callback URL.
2. Subscribe to the supported event types.
3. Validate incoming requests.
4. Process the payload and return a 2xx response.
5. Retry safely if the same event is delivered more than once.

## Endpoint Requirements

- Use HTTPS.
- Accept POST requests.
- Return a 2xx status code when processing succeeds.
- Make handlers idempotent.

## Operational Guidance

- Log failed deliveries.
- Queue heavy processing instead of blocking the response.
- Store event identifiers to prevent duplicate processing.

Webhook event definitions and payload formats should be documented alongside the relevant API capabilities as they become available.
