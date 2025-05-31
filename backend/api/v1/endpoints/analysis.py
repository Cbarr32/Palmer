from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.orm import Session
from typing import List, Dict, Any
from backend.core.database import get_db
from backend.services.analysis_service import AnalysisService
from backend.models.analysis import AnalysisRequest, QuickScanRequest, AnalysisResponse
from backend.core.auth import get_current_user
from backend.models.database import User

router = APIRouter()
analysis_service = AnalysisService()

@router.post("/quick-scan", response_model=Dict[str, Any])
async def quick_scan(
    request: QuickScanRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Perform a 30-60 second quick scan of a website"""
    try:
        result = await analysis_service.quick_scan(request.target_url)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/comprehensive", response_model=AnalysisResponse)
async def comprehensive_analysis(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Perform comprehensive multi-agent analysis"""
    try:
        # Start analysis
        analysis_id = await analysis_service.start_comprehensive_analysis(
            request, current_user.organization_id, db
        )
        
        # Run in background
        background_tasks.add_task(
            analysis_service.run_comprehensive_analysis,
            analysis_id, request, db
        )
        
        return {"analysis_id": analysis_id, "status": "processing"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/status/{analysis_id}")
async def get_analysis_status(
    analysis_id: str,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get the status of an ongoing analysis"""
    analysis = db.query(Analysis).filter(
        Analysis.id == analysis_id,
        Analysis.organization_id == current_user.organization_id
    ).first()
    
    if not analysis:
        raise HTTPException(status_code=404, detail="Analysis not found")
    
    return {
        "id": analysis.id,
        "status": analysis.status,
        "created_at": analysis.created_at,
        "completed_at": analysis.completed_at,
        "results": analysis.results if analysis.status == "completed" else None
    }

@router.get("/history")
async def get_analysis_history(
    skip: int = 0,
    limit: int = 10,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get analysis history for the organization"""
    analyses = db.query(Analysis).filter(
        Analysis.organization_id == current_user.organization_id
    ).offset(skip).limit(limit).all()
    
    return analyses
