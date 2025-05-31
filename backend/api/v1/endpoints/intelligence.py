from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from backend.core.database import get_db
from backend.services.intelligence_service import IntelligenceService
from backend.core.auth import get_current_user
from backend.models.database import User, Intelligence

router = APIRouter()
intelligence_service = IntelligenceService()

@router.post("/industry-report")
async def generate_industry_report(
    industry: str,
    competitors: List[str],
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Generate comprehensive industry intelligence report"""
    try:
        # Create intelligence record
        intel = Intelligence(
            organization_id=current_user.organization_id,
            intelligence_type="industry_report",
            status="processing"
        )
        db.add(intel)
        db.commit()
        
        # Generate in background
        background_tasks.add_task(
            intelligence_service.generate_industry_report,
            industry, competitors, intel.id, db
        )
        
        return {"intelligence_id": intel.id, "status": "processing"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/insights/{organization_id}")
async def get_organization_insights(
    organization_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get AI-generated insights for an organization"""
    if current_user.organization_id != organization_id:
        raise HTTPException(status_code=403, detail="Access denied")
    
    insights = db.query(Intelligence).filter(
        Intelligence.organization_id == organization_id
    ).order_by(Intelligence.created_at.desc()).limit(10).all()
    
    return insights

@router.post("/predict")
async def predict_market_trends(
    industry: str,
    timeframe: str = "6_months",
    current_user: User = Depends(get_current_user)
):
    """Generate market predictions"""
    predictions = {
        "industry": industry,
        "timeframe": timeframe,
        "predictions": [
            {
                "trend": "AI adoption",
                "probability": 0.85,
                "impact": "high",
                "recommendation": "Invest in AI capabilities"
            },
            {
                "trend": "Mobile-first shift",
                "probability": 0.92,
                "impact": "medium",
                "recommendation": "Optimize mobile experience"
            }
        ],
        "opportunities": [
            "Early AI adoption advantage",
            "Underserved mobile segment",
            "Partnership opportunities"
        ]
    }
    return predictions
