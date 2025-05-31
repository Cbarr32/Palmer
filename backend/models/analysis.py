from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Any, Optional
from datetime import datetime

class QuickScanRequest(BaseModel):
    target_url: HttpUrl

class AnalysisRequest(BaseModel):
    target_url: HttpUrl
    competitors: List[HttpUrl] = []
    analysis_depth: str = "standard"
    include_predictions: bool = True
    generate_report: bool = True

class AnalysisResponse(BaseModel):
    id: str
    target_url: str
    competitors: List[str]
    competitive_analysis: Dict[str, Any]
    technology_analysis: Dict[str, Any]
    customer_insights: Dict[str, Any]
    predictions: Dict[str, Any]
    synthesis: Dict[str, Any]
    timestamp: datetime
    
class CompetitorSuggestion(BaseModel):
    url: str
    relevance_score: float
    reasoning: str
