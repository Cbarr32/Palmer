from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from backend.core.database import get_db, engine
from sqlalchemy import text
import asyncio
from datetime import datetime

router = APIRouter()

@router.get("/")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "service": "Palmer Intelligence API",
        "version": "1.0.0"
    }

@router.get("/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """Detailed health check including database"""
    checks = {
        "api": "healthy",
        "database": "unknown",
        "agents": "unknown"
    }
    
    # Check database
    try:
        db.execute(text("SELECT 1"))
        checks["database"] = "healthy"
    except Exception as e:
        checks["database"] = f"unhealthy: {str(e)}"
    
    # Check agents
    try:
        from backend.agents.base_agent import BaseAgent
        agent = BaseAgent()
        checks["agents"] = "healthy"
    except Exception as e:
        checks["agents"] = f"unhealthy: {str(e)}"
    
    overall_status = "healthy" if all(v == "healthy" for v in checks.values()) else "unhealthy"
    
    return {
        "status": overall_status,
        "timestamp": datetime.utcnow().isoformat(),
        "checks": checks
    }
