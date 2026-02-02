# 🍯 AI Agentic Honeypot System

A complete AI-powered scam detection and engagement system that uses machine learning to detect scams, engage with scammers through conversational AI, and extract intelligence information.

## 🎯 Features

- **Multilingual Scam Detection**: Supports English, Hindi, Tamil, Telugu, and Malayalam
- **AI Conversation Agent**: GPT-4 powered agent that naturally engages scammers
- **Intelligence Extraction**: Automatically extracts bank accounts, UPI IDs, phone numbers, and phishing links
- **Real-time Dashboard**: Interactive UI for testing and monitoring
- **Session Management**: Redis-based conversation tracking
- **Evaluation Callback**: Reports results to external API endpoint

## 🏗️ Architecture

```
honeypot-system/
├── backend/              # FastAPI REST API
│   ├── app/
│   │   ├── api/         # API routes and authentication
│   │   ├── core/        # Scam detection, AI agent, extraction
│   │   ├── models/      # Pydantic schemas
│   │   └── utils/       # Session management, callbacks
│   └── requirements.txt
├── frontend/             # React dashboard
│   ├── src/
│   │   ├── components/  # UI components
│   │   ├── pages/       # Dashboard page
│   │   └── services/    # API client
│   └── package.json
└── docker-compose.yml
```

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- Node.js 18+
- Redis (or use Docker)
- OpenAI API key

### Option 1: Using Docker (Recommended)

1. **Clone and setup**:
   ```bash
   cd C:\Users\admin\honeypot
   cp .env.example .env
   ```

2. **Configure environment variables** in `.env`:
   ```env
   API_SECRET_KEY=your_secret_key_here
   OPENAI_API_KEY=sk-your-openai-api-key-here
   CALLBACK_URL=https://hackathon.guvi.in/api/updateHoneyPotFinalResult
   ```

3. **Start all services**:
   ```bash
   docker-compose up
   ```

4. **Access the application**:
   - Frontend: http://localhost:5173
   - Backend API: http://localhost:8000
   - API Docs: http://localhost:8000/docs

### Option 2: Manual Setup

#### Backend Setup

1. **Navigate to backend**:
   ```bash
   cd backend
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv venv
   .\venv\Scripts\activate  # Windows
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**:
   ```bash
   cp ..\.env.example .env
   # Edit .env with your API keys
   ```

5. **Start Redis** (in separate terminal):
   ```bash
   redis-server
   ```

6. **Run backend**:
   ```bash
   python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
   ```

#### Frontend Setup

1. **Navigate to frontend**:
   ```bash
   cd frontend
   ```

2. **Install dependencies**:
   ```bash
   npm install
   ```

3. **Configure environment**:
   ```bash
   cp .env.example .env
   # Edit .env with backend URL and API key
   ```

4. **Run frontend**:
   ```bash
   npm run dev
   ```

## 📡 API Documentation

### POST /api/detect-scam

Detect scams and engage with scammers.

**Headers**:
```
Content-Type: application/json
x-api-key: YOUR_API_KEY
```

**Request Body**:
```json
{
  "sessionId": "session-123",
  "message": {
    "sender": "scammer",
    "text": "Your account will be blocked! Verify now.",
    "timestamp": "2026-02-01T10:00:00Z"
  },
  "conversationHistory": [],
  "metadata": {
    "channel": "SMS",
    "language": "English",
    "locale": "IN"
  }
}
```

**Response**:
```json
{
  "status": "success",
  "scamDetected": true,
  "engagementMetrics": {
    "engagementDurationSeconds": 30,
    "totalMessagesExchanged": 1
  },
  "extractedIntelligence": {
    "bankAccounts": [],
    "upids": [],
    "phishingLinks": ["http://bit.ly/verify"],
    "phoneNumbers": [],
    "suspiciousKeywords": ["blocked", "verify", "urgent"]
  },
  "agentNotes": "Engaged scammer for 1 messages...",
  "agentResponse": "I'm concerned about this. Can you provide more details?"
}
```

### Additional Endpoints

- `GET /health` - Health check
- `GET /api/session/{sessionId}` - Get session data
- `POST /api/reset-session/{sessionId}` - Reset session

## 🧪 Testing

### Using the Dashboard

1. **Load Sample Scenario**:
   - Select a scenario (Bank Fraud, UPI Fraud, etc.)
   - Click "Load Scenario"
   - Watch the AI agent engage automatically

2. **Manual Testing**:
   - Type scammer messages in the chat
   - Enable "Auto-respond mode" for automatic AI responses
   - View extracted intelligence in real-time

3. **Export Results**:
   - Click "Export Results" to download session data as JSON

### Using cURL

```bash
curl -X POST http://localhost:8000/api/detect-scam \
  -H "Content-Type: application/json" \
  -H "x-api-key: your_secret_key_here" \
  -d @test_payload.json
```

## 🎨 Sample Test Scenarios

The system includes 6 pre-configured test scenarios:

1. **Bank Fraud**: Account blocking urgency scam
2. **UPI Fraud**: Payment refund scam
3. **Phishing**: Prize/lottery winner scam
4. **Tech Support**: Fake virus/tech support scam
5. **Romance Scam**: Emergency money request
6. **Hindi Bank Fraud**: Hindi language banking scam

## 🔧 Configuration

### Backend Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `API_SECRET_KEY` | API authentication key | Yes |
| `OPENAI_API_KEY` | OpenAI API key for GPT-4 | Yes |
| `REDIS_URL` | Redis connection URL | No (defaults to localhost) |
| `CALLBACK_URL` | Evaluation callback endpoint | Yes |

### Frontend Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| `VITE_API_URL` | Backend API URL | Yes |
| `VITE_API_KEY` | API key for authentication | Yes |

## 🚢 Deployment

### Backend Deployment (Render/Railway)

1. Connect your GitHub repository
2. Set environment variables
3. Deploy command: `uvicorn app.main:app --host 0.0.0.0 --port 8000`

### Frontend Deployment (Vercel/Netlify)

1. Connect your GitHub repository
2. Build command: `npm run build`
3. Publish directory: `dist`
4. Set environment variables

### Redis Hosting

Use a managed Redis service:
- **Upstash** (Free tier available)
- **Redis Cloud**
- **AWS ElastiCache**

## 📊 System Components

### 1. Scam Detection Engine
- Rule-based multilingual pattern matching
- Urgency detection
- Impersonation detection
- Financial request detection
- Confidence scoring

### 2. AI Conversation Agent
- GPT-4 powered responses
- Natural engagement strategy
- Intelligence extraction focus
- Language-aware responses

### 3. Intelligence Extractor
- Bank account regex patterns
- UPI ID extraction
- Phone number detection
- URL/phishing link extraction
- Keyword aggregation

### 4. Session Manager
- Redis-based storage
- Conversation history tracking
- Metrics accumulation
- Automatic expiry

### 5. Callback System
- Async reporting to evaluation endpoint
- Retry logic
- Trigger criteria checking

## 🎯 Evaluation Callback

The system automatically sends results to:
```
POST https://hackathon.guvi.in/api/updateHoneyPotFinalResult
```

**Payload**:
```json
{
  "sessionId": "session-123",
  "scamDetected": true,
  "totalMessagesExchanged": 10,
  "extractedIntelligence": { ... },
  "agentNotes": "Successfully extracted 2 UPI IDs..."
}
```

## 🛠️ Development

### Project Structure

- **Backend**: FastAPI with async support
- **Frontend**: React 18 with Vite
- **Styling**: Tailwind CSS with custom design system
- **State**: React hooks
- **API Client**: Axios
- **AI**: OpenAI GPT-4
- **Storage**: Redis

### Adding New Scam Patterns

Edit `backend/app/core/detector.py`:

```python
URGENCY_PATTERNS = {
    'English': [r'new_pattern_here'],
    # Add more languages...
}
```

### Adding New Test Scenarios

Edit `frontend/src/services/scenarios.js`:

```javascript
export const SAMPLE_SCENARIOS = {
  'New Scenario': {
    messages: [...],
    language: 'English',
    channel: 'SMS'
  }
}
```

## 📝 License

This project is created for the GUVI Hackathon.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Open a Pull Request

## 📞 Support

For issues or questions:
- Check the API documentation at `/docs`
- Review the logs in the dashboard
- Test with sample scenarios first

## 🎉 Acknowledgments

- OpenAI for GPT-4 API
- FastAPI framework
- React and Vite
- Redis for session management
- Tailwind CSS for styling

---

Built with ❤️ for scam detection and prevention
