# Firebase Firestore Setup Guide

This project uses **Firebase Firestore** (NoSQL database) for persistent logging of:
- Session data and metadata
- Conversation history (chat logs)
- Detected scam intelligence
- API request logs and analytics

## 1. Create a Firebase Project

1. Go to [Firebase Console](https://console.firebase.google.com/).
2. Click **"Add project"**.
3. Name your project (e.g., `honeypot-scam-detection`).
4. (Optional) Disable Google Analytics for simplicity.
5. Click **"Create project"**.

## 2. Enable Firestore Database

1. In the left sidebar, go to **Build** → **Firestore Database**.
2. Click **"Create database"**.
3. Select **Production mode**.
4. Choose a location close to your users (e.g., `us-central1`).
5. Click **"Enable"**.

## 3. Generate Service Account Credentials

The backend needs a Service Account to write to Firestore securely.

1. Click the **Settings gear icon** (next to Project Overview) → **Project settings**.
2. Go to the **Service accounts** tab.
3. Click **"Generate new private key"**.
4. Click **"Generate key"** to download the JSON file.

> **⚠️ SECURITY WARNING:** Never commit this JSON file to Git!

## 4. Configure Environment Variables

You need to extract values from the JSON file and set them as environment variables.

Open the downloaded JSON file and look for these fields:

```json
{
  "type": "service_account",
  "project_id": "...",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...",
  "client_email": "...",
  "client_id": "...",
  "auth_uri": "...",
  "token_uri": "...",
  "auth_provider_x509_cert_url": "...",
  "client_x509_cert_url": "..."
}
```

Add them to your `.env` file (locally) or Render Environment Dashboard:

```env
FIREBASE_TYPE=service_account
FIREBASE_PROJECT_ID=<project_id>
FIREBASE_PRIVATE_KEY_ID=<private_key_id>
FIREBASE_PRIVATE_KEY=<private_key>  # Copy the whole string including \n
FIREBASE_CLIENT_EMAIL=<client_email>
FIREBASE_CLIENT_ID=<client_id>
FIREBASE_AUTH_URI=https://accounts.google.com/o/oauth2/auth
FIREBASE_TOKEN_URI=https://oauth2.googleapis.com/token
FIREBASE_AUTH_PROVIDER_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
FIREBASE_CLIENT_CERT_URL=<client_x509_cert_url>
```

> **Note for Render:** When adding `FIREBASE_PRIVATE_KEY` in Render, simply paste the entire value. Render handles newlines correctly.

## 5. Verify Setup

Start the backend:
```bash
docker-compose up backend
```

Check the logs for:
```
Firebase initialized successfully for project: your-project-id
```

## 6. Firestore Data Structure

Your data will appear in these collections:

- **`sessions`**: Active and past sessions.
  - Subcollection **`conversations`**: Individual messages.
- **`scam_intelligence`**: Detected scams and extracted data.
- **`api_logs`**: Request/response logs for debugging.

## Troubleshooting

- **"Firebase initialization skipped"**: Check if you missed any environment variables.
- **"Permission denied"**: Ensure your Service Account has "Firebase Admin" or "Cloud Datastore User" roles (default owner has these).
- **Newline errors**: Ensure `FIREBASE_PRIVATE_KEY` is quoted properly in `.env`.
