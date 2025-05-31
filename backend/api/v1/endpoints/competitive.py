from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from backend.core.database import get_db
from backend.services.intelligence_service import IntelligenceService
from backend.core.auth import get_current_user
from backend.models.database import User

router = APIRouter()
intelligence_service = IntelligenceService()

@router.post("/analyze")
async def analyze_competitors(
    target_url: str,
    competitors: List[str],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Analyze competitive landscape"""
    try:
        result = await intelligence_service.competitive_intelligence(
            target_url, competitors
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/suggestions/{target_url}")
async def get_competitor_suggestions(
    target_url: str,
    current_user: User = Depends(get_current_user)
):
    """Get AI-suggested competitors for a target URL"""
    # Simplified for now - in production, this would use ML
    return {
        "target": target_url,
        "suggested_competitors": [
            "competitor1.com",
            "competitor2.com",
            "competitor3.com"
        ]
    }

@router.post("/benchmark")
async def benchmark_performance(
    target_url: str,
    metrics: List[str],
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Benchmark against industry standards"""
    return {
        "target": target_url,
        "benchmarks": {
            "performance": {"score": 85, "industry_avg": 70},
            "seo": {"score": 90, "industry_avg": 75},
            "ux": {"score": 88, "industry_avg": 80}
        }
    }
