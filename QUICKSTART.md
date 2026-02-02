# 🚀 Quick Start Guide

## Prerequisites Check
- ✅ Python 3.13.5 (Detected)
- ✅ Node.js v24.13.0 (Detected)
- ⚠️ OpenAI API Key (Required - see setup below)
- ⚠️ Redis (Optional - will use in-memory fallback)

## Step 1: Configure OpenAI API Key

1. Get your API key from: https://platform.openai.com/api-keys

2. Edit the `.env` file in the honeypot directory:
   ```env
   OPENAI_API_KEY=sk-your-actual-api-key-here
   ```

## Step 2: Install Backend Dependencies

Open PowerShell/Terminal in the honeypot directory:

```powershell
# Navigate to backend
cd backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
.\venv\Scripts\activate  # Windows
# or
source venv/bin/activate  # Linux/Mac

# Install dependencies
pip install -r requirements.txt
```

## Step 3: Install Frontend Dependencies

Open a NEW PowerShell/Terminal window:

```powershell
# Navigate to frontend
cd frontend

# Install dependencies
npm install
```

## Step 4: Start the Backend Server

In the first terminal (with venv activated):

```powershell
cd backend
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

You should see:
```
INFO:     Uvicorn running on http://0.0.0.0:8000
```

## Step 5: Start the Frontend Server

In the second terminal:

```powershell
cd frontend
npm run dev
```

You should see:
```
VITE ready in XXX ms
Local: http://localhost:5173/
```

## Step 6: Test the System

1. **Open browser**: http://localhost:5173

2. **Load a test scenario**:
   - Select "Bank Fraud" from dropdown
   - Click "Load Scenario"
   - Watch the AI agent respond automatically

3. **Check detection metrics**:
   - Scam Probability should show ~90%
   - Keywords should be highlighted
   - Extracted intelligence should appear

4. **Manual testing**:
   - Type your own scammer message
   - Enable "Auto-respond mode"
   - Send and watch AI engage

## Step 7: Test API Directly (Optional)

In a third terminal:

```powershell
# Test health endpoint
curl http://localhost:8000/health

# Test scam detection
curl -X POST http://localhost:8000/api/detect-scam ^
  -H "Content-Type: application/json" ^
  -H "x-api-key: honeypot_demo_key_2026" ^
  -d @test_payload.json
```

## Troubleshooting

### Backend won't start
- Check Python version: `python --version`
- Ensure venv is activated (you should see `(venv)` in prompt)
- Check .env file has OPENAI_API_KEY set

### Frontend won't start
- Check Node version: `node --version`
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Check .env file exists in frontend directory

### API returns 401 Unauthorized
- Check x-api-key header matches .env: `honeypot_demo_key_2026`

### AI Agent not responding
- Check OPENAI_API_KEY is valid in .env
- Check backend logs for errors
- Verify OpenAI API has credits

### Redis connection errors
- Don't worry! System will use in-memory storage as fallback
- For production, install Redis or use Upstash

## Next Steps

1. **Customize**: Edit scam detection patterns in `backend/app/core/detector.py`
2. **Add scenarios**: Edit `frontend/src/services/scenarios.js`
3. **Deploy**: Follow README.md deployment section
4. **Monitor**: Check API logs in dashboard

## Sample Test Flow

1. Start both servers
2. Open http://localhost:5173
3. Select "Bank Fraud" scenario
4. Click "Load Scenario"
5. Watch conversation unfold
6. View extracted intelligence
7. Click "Export Results" to save
8. Try other scenarios!

---

Need help? Check the full README.md for detailed documentation.
