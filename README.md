# Palmer Intelligence Platform

AI-powered competitive analysis and market intelligence platform using Anthropic's Claude.

## Setup

### Backend Setup

1. Install Python dependencies:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

2. Set your Anthropic API key in `.env`:
```
ANTHROPIC_API_KEY=your_actual_api_key_here
```

3. Run the backend:
```bash
python main.py
```

The API will be available at http://localhost:8000
API documentation at http://localhost:8000/api/v1/docs

### Frontend Setup

1. Install Node dependencies:
```bash
cd frontend
npm install
```

2. Run the frontend:
```bash
npm run dev
```

The frontend will be available at http://localhost:3000

## Features

- Quick website analysis (30-60 seconds)
- Comprehensive competitive analysis
- Technology stack detection
- Customer sentiment analysis
- Market predictions
- Industry reports

## API Endpoints

- `POST /api/v1/analysis/quick-scan` - Quick website analysis
- `POST /api/v1/analysis/comprehensive` - Full competitive analysis
- `POST /api/v1/competitive/analyze` - Competitive landscape analysis
- `POST /api/v1/intelligence/industry-report` - Industry intelligence report
- `GET /api/v1/health` - Health check

## Architecture

- **Backend**: FastAPI with Anthropic Claude integration
- **Frontend**: Next.js with TypeScript and Tailwind CSS
- **AI Agents**: Multiple specialized agents for different analysis types
  - Competitive Intelligence Agent
  - Technology Reconnaissance Agent
  - Customer Voice Agent
  - Prediction Learning Agent
