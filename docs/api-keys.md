# API Keys

API keys identify your application and authorize access to the LanguageCheck API.

## Generate a Key

Create a key from the LanguageCheck developer area or the provisioning flow provided by your team.

When a new key is created, record it immediately and store it securely. Treat it like any other production secret.

## Key Management

- Create separate keys for each environment.
- Assign one key per application or service when possible.
- Revoke keys that are no longer in use.
- Rotate keys during scheduled maintenance windows.

## Security Notes

- Do not commit keys to source control.
- Do not embed keys in mobile or browser-distributed code.
- Monitor usage to detect unexpected traffic patterns.

## Next Step

After generating a key, continue to the authentication guide to attach it to your requests.
