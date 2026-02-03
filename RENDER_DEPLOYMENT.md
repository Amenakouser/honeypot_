# Render Deployment Guide

## Environment Variables Required

Set these in your Render dashboard:

1. **API_SECRET_KEY** - Your API authentication key
2. **OPENAI_API_KEY** - Your OpenAI API key (starts with sk-)
3. **CALLBACK_URL** - https://hackathon.guvi.in/api/updateHoneyPotFinalResult
4. **REDIS_URL** - Auto-populated from Redis service

## Deployment Steps

### Option 1: Using render.yaml (Recommended)

1. Push your code to GitHub
2. In Render dashboard, click "New" → "Blueprint"
3. Connect your repository
4. Render will automatically detect `render.yaml`
5. Set the required environment variables
6. Click "Apply"

### Option 2: Manual Setup

1. **Create Redis Service**:
   - Click "New" → "Redis"
   - Name: `honeypot-redis`
   - Plan: Free
   - Click "Create Redis"

2. **Create Web Service**:
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
   
3. **Environment Variables**:
   Add these in the "Environment" section:
   ```
   API_SECRET_KEY=<your-secret-key>
   OPENAI_API_KEY=<your-openai-key>
   CALLBACK_URL=https://hackathon.guvi.in/api/updateHoneyPotFinalResult
   REDIS_URL=<copy-from-redis-service-internal-url>
   ```

4. **Deploy**:
   - Click "Create Web Service"
   - Wait for deployment to complete

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
