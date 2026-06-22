# Nylas Webhook Troubleshooting Guide

## What You're Setting Up

In this part of the project, you're connecting your local development server to Nylas using a webhook. A webhook is how Nylas notifies your app in real-time when new emails arrive or updates happen.

Since your local machine isn't publicly accessible from the internet, we use a **tunnel** (like Pinggy or Cloudflare) to temporarily expose your local port (for example, port 8000) to a public URL. Nylas sends its webhook events to this public URL, which then forwards the requests to your local app.

This setup is temporary and mainly for testing during development. In production, you'd deploy the app to a server with a fixed URL.

## The Goal

You're configuring the webhook so that Nylas can successfully send event notifications to your `/events` endpoint without returning a `401 Unauthorized` error. When everything works correctly:

- The webhook registers successfully in Nylas
- The secret key matches between your app and Nylas
- You can see event logs appearing in your terminal when emails are received

## Common Issues and Fixes

### 1. Environment Variables Not Loading

**Symptoms:** You get a `401 Unauthorized` error or the app doesn't pick up new Pinggy URLs or secrets.

**Fix:**
The latest version of the repo already includes this line in `main.py`:

```python
load_dotenv(override=True)
```

If you edited or copied earlier code, make sure this line exists at the top of main.py and all config scripts. If it still doesn't work, restart your IDE (like VS Code or Cursor) to clear cached environment variables.

### 2. Expired Pinggy URL

Pinggy URLs expire every 60 minutes, so you'll need to reconfigure them. Some students also reported success using [Serveo](https://serveo.net/) as a backup tunnel; the steps below still apply, just replace the tunneling command with the Serveo variant if needed.

**Fix:**
1. Delete the old webhook in the Nylas dashboard under Notifications
2. Run the Pinggy tunnel again:

```bash
ssh -p 443 -R0:localhost:8000 free.pinggy.io
```

If you're on Windows, use:

```bash
ssh -p 443 -R0:127.0.0.1:8000 free.pinggy.io
```

3. Copy the new Pinggy URL (HTTPS) into the .env file as SERVER_URL
4. Clear out the old WEBHOOK_SECRET
5. Run:

```bash
uv run app/main.py
uv run app/config/config_webhook.py
```

6. Copy the new secret from the terminal or Nylas dashboard into your .env file
7. Restart the server:

```bash
uv run app/main.py
```

### 3. Firewall or VPN Interference

**Symptoms:** You can't connect to Pinggy or the webhook fails to verify.

**Fix:**
- Disable antivirus, firewall, or VPN temporarily
- If you're using a corporate or school network, try a personal hotspot instead

### 4. Webhook Secret Sync Failure

**Symptoms:** The webhook registers, but Nylas fails to authenticate (401).

**Fixes that have worked for others:**
- Delete the webhook and recreate it manually in the Nylas UI, then copy the secret into .env
- Make sure WEBHOOK_SECRET matches exactly between Nylas and your local .env
- Ensure you've restarted your server after updating .env

### 5. Port Conflicts

**Symptoms:** Nothing happens when you run main.py, or Pinggy can't forward requests.

**Fix:**
- Try a different port, like 8080 or 8085
- Update both your .env and your Pinggy command to match:

```bash
ssh -p 443 -R0:127.0.0.1:8085 free.pinggy.io
```

## Summary of Working Steps

If you're still stuck, follow this checklist exactly:

1. Kill any old main.py processes
2. Run the Pinggy command and copy the new URL
3. Update .env:
   - `SERVER_URL = your Pinggy URL` (**Make sure to use the HTTPS URL, not HTTP!**)
   - Clear `WEBHOOK_SECRET`
4. Run:

```bash
uv run app/main.py
uv run app/config/config_webhook.py
```

5. Copy the secret from the output into .env
6. Restart your IDE and rerun main.py
7. Test by sending yourself an email. You should see webhook events appear in your terminal

## Notes from the Community

- Some Windows users needed to use `127.0.0.1` instead of `localhost`
- Nylas blocks ngrok, so don't use it
- If you see 500 errors, check that your Pydantic model allows optional fields (e.g. `snippet: Optional[str] = None`)
- If you're using VS Code or Cursor, always restart the terminal after updating .env

With these fixes, your webhook should register and work consistently. The main issue was outdated environment variables not being reloaded, which is now fixed in the updated repository.

