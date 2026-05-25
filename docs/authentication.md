# Authentication

LanguageCheck API uses API key authentication.

Include your API key in the request headers for every call to the API. Requests without a valid key are rejected.

## How It Works

1. Generate an API key from your developer workspace.
2. Store the key securely in your application configuration.
3. Send the key with each API request.
4. Rotate the key if you suspect exposure.

## Recommended Practices

- Never expose API keys in client-side applications.
- Store secrets in environment variables or a secret manager.
- Use separate keys for development and production.
- Rotate keys regularly.

## Example

```http
Authorization: Bearer YOUR_API_KEY
```

If your integration uses a different header convention, follow the contract defined by the API reference and your issued credentials.
