# Gmail API Quick Setup Guide

## Prerequisites
- Google account
- Python environment with `langchain-google-community[gmail]` installed

## 1. Google Cloud Console Setup (5 minutes)

### Create Project & Enable API
```bash
# Go to: https://console.cloud.google.com/
```
1. **New Project** → Enter name → **Create**
2. **APIs & Services** → **Library** → Search "Gmail API" → **Enable**

### Configure OAuth Consent
3. **APIs & Services** → **OAuth consent screen**
4. **External** → **Create**
5. Fill required fields:
   - App name: "My Gmail App"
   - User support email: your email
   - Developer contact: your email
6. **Save and Continue** → Skip "Scopes" → **Save and Continue**
7. **Test users** → **Add Users** → Enter email addresses → **Save**
8. **Save and Continue** → **Back to Dashboard**

### Create Credentials
9. **APIs & Services** → **Credentials** → **Create Credentials** → **OAuth client ID**
10. **Desktop application** → Name: "Gmail Client" → **Create**
11. **Download JSON** → Save as `credentials.json`

## 2. Python Implementation

### Basic Setup
```python
from langchain_google_community.gmail.utils import (
    build_resource_service,
    get_gmail_credentials,
)
from langchain_google_community.gmail.toolkit import GmailToolkit

# Authenticate (opens browser first time)
credentials = get_gmail_credentials(
    token_file="token.json",
    scopes=["https://www.googleapis.com/auth/gmail.readonly"],
    client_secrets_file="credentials.json",
)

# Create toolkit
api_resource = build_resource_service(credentials=credentials)
toolkit = GmailToolkit(api_resource=api_resource)

# Use tools
tools = toolkit.get_tools()
print([tool.name for tool in tools])
```

## 3. First Run Authentication

### Option A: Click Through Warning (Fastest)
1. Run your Python code
2. Browser opens with Google auth
3. **Click "Advanced"** → **"Go to [App Name] (unsafe)"** → **Continue**
4. Grant permissions
5. See "Authentication flow completed"

### Option B: Add Test Users (No Warning)
1. **Before running Python code**, go to Google Console
2. **APIs & Services** → **OAuth consent screen** → **Edit App**
3. **Test users** → **Add Users** → Enter email addresses
4. **Save** → Now run Python code (no warning for test users)

## Files Created
- `credentials.json` - Your app secrets (from Google Console)
- `token.json` - Access token (auto-generated after auth)

## Common Scopes
```python
# Read-only access
scopes=["https://www.googleapis.com/auth/gmail.readonly"]

# Full access
scopes=["https://www.googleapis.com/auth/gmail.modify"]

# Send emails
scopes=["https://www.googleapis.com/auth/gmail.send"]
```

## Troubleshooting
- **redirect_uri_mismatch**: Use "Desktop application", not "Web application"
- **App not verified warning**: Normal for development - click through it
- **Missing credentials.json**: Download from Google Console credentials page
- **Token expired**: Delete `token.json` and re-run to re-authenticate

## Adding Test Users Later

If you want to add test users after initial setup:

```bash
# Go to: https://console.cloud.google.com/
```

1. **APIs & Services** → **OAuth consent screen**
2. **Edit App** → **Test users** → **Add Users**
3. Enter Gmail addresses (one per line):
   ```
   user1@gmail.com
   user2@gmail.com
   developer@company.com
   ```
4. **Save** → Test users can now authenticate without warnings

**Note**: Test users have the same permissions as the developer. Only add trusted users.