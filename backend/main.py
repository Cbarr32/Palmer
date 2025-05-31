"""Palmer Intelligence - Advanced Competitive Intelligence Platform"""
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
from datetime import datetime
import logging
import os
from dotenv import load_dotenv

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Palmer Intelligence",
    description="AI-Powered Competitive Intelligence Platform",
    version="3.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "Palmer Intelligence - Advanced Competitive Intelligence",
        "version": "3.0.0",
        "capabilities": [
            "Multi-site competitive analysis",
            "Technology stack detection",
            "Social media intelligence",
            "Customer voice analysis",
            "Predictive intelligence",
            "Industry report generation"
        ],
        "api_docs": "/docs"
    }

@app.post("/api/v1/analyze")
async def analyze_competitors(target_url: str):
    return {"status": "analyzing", "target": target_url}

@app.post("/api/v1/industry-report")
async def generate_industry_report(industry: str, companies: List[str]):
    return {"status": "generating", "industry": industry}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
