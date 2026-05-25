# SDKs

LanguageCheck API can be integrated from any environment that can make HTTPS requests.

Official SDK availability depends on your current plan and release stage. If no SDK is available for your language, use the REST API directly.

## Integration Options

- Direct HTTP integration for full control.
- Internal wrappers maintained by your team.
- Future official SDKs for common languages and platforms.

## What an SDK Should Cover

- Authentication handling
- Request serialization
- Response parsing
- Error mapping
- Retry and timeout configuration

## Recommendation

Start with a thin internal client around the API reference. This makes it easier to adopt an official SDK later without changing the rest of your application.
