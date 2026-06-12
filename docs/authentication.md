# Authentication

LanguageCheck API uses API key authentication.

Send a valid API key in the `X-Api-Key` header for every API request.

## Required Header

```http
X-Api-Key: YOUR_API_KEY
```

- `YOUR_API_KEY` must be a valid, active key generated from the Developers page.
- Revoked, invalid, or malformed keys are rejected.

## cURL Example

```bash
curl -X POST "https://api.languagecheck.ai/v2/..." \
	-H "Content-Type: application/json" \
	-H "X-Api-Key: YOUR_API_KEY" \
	-d '{"source":"...","target":"..."}'
```

## Error Behavior

- Missing `X-Api-Key` header: request is rejected.
- Invalid or revoked key: request is rejected.
- Key without required access scope (for future protected resources): request is rejected.

Refer to endpoint-specific responses in the API reference for exact status codes and payload format.

## Security Notes

- Keep API keys server-side only.
- Never expose keys in frontend apps, logs, or source control.
- Use separate keys per environment and integration.
- Rotate keys regularly, and immediately if exposure is suspected.

## Related

See the API Keys page for generation, visibility, and revocation rules.

## Documentation Portal Sign-In

The documentation portal supports Firebase sign-in with Google and Email/Password.

This sign-in is for the docs website session only and is independent from API authentication.
API requests still require a valid `X-Api-Key` header.
