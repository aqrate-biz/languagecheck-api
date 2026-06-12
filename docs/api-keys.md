# API Keys

API keys let your applications authenticate with the LanguageCheck API.

## Who Can Create API Keys

You must:

- Be logged in to https://languagecheck.ai
- Have a Pro plan, or be part of a Team Enterprise workspace

In Team Enterprise, only users with the proper team permission can create team-wide API keys.

## Where to Create Keys

1. Log in to LanguageCheck.
2. Open the user menu.
3. Select **Developers**.
4. Open the API Keys page.
5. Click **Generate API Key**.

## Important Behavior

- The full API key is shown only once, at creation time.
- You can create multiple keys.
- You can revoke keys you no longer need.
- If you are a Team user with permission, you can create keys that work for the entire team.

## Recommended Usage

- Create separate keys for development, staging, and production.
- Use one key per app or integration to simplify revocation.
- Save keys in a secret manager or environment variables.
- Never share keys in chat, tickets, screenshots, or email.
- Never commit keys to source control.

## Rotation and Revocation

- Rotate keys regularly and immediately if exposure is suspected.
- When rotating, create a new key first, deploy it, then revoke the old key.
- Revoke unused or temporary keys as soon as possible.

## Troubleshooting

- If you do not see **Developers** page, check your plan and account role.
- If a key is lost, generate a new one; the original cannot be displayed again.
