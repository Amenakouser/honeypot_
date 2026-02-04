# Render Deployment Guide

## Environment Variables Required

### Backend Service

Set these in your Render dashboard for the backend:

1. **API_SECRET_KEY** - Your API authentication key
2. **OPENAI_API_KEY** - Your OpenAI API key (starts with sk-)
3. **CALLBACK_URL** - https://hackathon.guvi.in/api/updateHoneyPotFinalResult
4. **REDIS_URL** - Auto-populated from Redis service

### Frontend Service

Set these in your Render dashboard for the frontend:

1. **VITE_API_KEY** - Same value as API_SECRET_KEY
2. **VITE_API_URL** - Auto-populated from backend service URL

## Deployment Steps

### Option 1: Using render.yaml (Recommended)

1. Push your code to GitHub
2. In Render dashboard, click "New" → "Blueprint"
3. Connect your repository
4. Render will automatically detect `render.yaml` and create:
   - Backend web service (Python/FastAPI)
   - Frontend web service (React/Nginx)
   - Redis service
5. Set the required environment variables for each service
6. Click "Apply"

### Option 2: Manual Setup

#### 1. Create Redis Service

- Click "New" → "Redis"
- Name: `honeypot-redis`
- Plan: Free
- Click "Create Redis"

#### 2. Create Backend Web Service

- Click "New" → "Web Service"
- Connect your GitHub repository
- Settings:
  - Name: `honeypot-backend`
  - Region: Oregon (or your preferred region)
  - Branch: `main`
  - Root Directory: Leave empty
  - Runtime: Docker
  - Dockerfile Path: `./backend/Dockerfile`
  - Docker Context: `./backend`
  - Plan: Free

- Environment Variables:
  ```
  API_SECRET_KEY=<your-secret-key>
  OPENAI_API_KEY=<your-openai-key>
  CALLBACK_URL=https://hackathon.guvi.in/api/updateHoneyPotFinalResult
  REDIS_URL=<copy-from-redis-service-internal-url>
  ```

  **Firebase Credentials:**
  Extract values from your Service Account JSON file and add:
  ```
  FIREBASE_TYPE=service_account
  FIREBASE_PROJECT_ID=<project_id>
  FIREBASE_PRIVATE_KEY=<private_key> (Paste the entire key including \n)
  FIREBASE_CLIENT_EMAIL=<client_email>
  FIREBASE_CLIENT_ID=<client_id>
  # Add other FIREBASE_ vars from JSON...
  ```

- Click "Create Web Service"

- Click "Create Web Service"

#### 3. Create Frontend Web Service

- Click "New" → "Web Service"
- Connect your GitHub repository
- Settings:
  - Name: `honeypot-frontend`
  - Region: Oregon
  - Branch: `main`
  - Root Directory: Leave empty
  - Runtime: Docker
  - Dockerfile Path: `./frontend/Dockerfile`
  - Docker Context: `./frontend`
  - Plan: Free

- Environment Variables:
  ```
  VITE_API_KEY=<same-as-backend-API_SECRET_KEY>
  VITE_API_URL=<backend-service-url>
  ```

- Click "Create Web Service"

## Troubleshooting

### Build Fails
- Check that all environment variables are set
- Verify Dockerfile path is correct: `./backend/Dockerfile`
- Ensure Docker context is: `./backend`

### Health Check Fails
- Verify `/health` endpoint is accessible
- Check logs for startup errors
- Ensure PORT environment variable is being used

### Redis Connection Issues
- Use the internal Redis URL from Render
- Format: `redis://red-xxxxx:6379`
- Don't use external URL (it requires paid plan)

## Verifying Deployment

1. Check health endpoint: `https://your-app.onrender.com/health`
2. View API docs: `https://your-app.onrender.com/docs`
3. Test root endpoint: `https://your-app.onrender.com/`

## Auto-Deploy

Render will automatically deploy when you push to the `main` branch.

## Logs

View logs in Render dashboard → Your Service → Logs tab
