"""Palmer Intelligence API - Advanced Competitive Intelligence Platform"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import logging
from api.routes import analysis, competitive_analysis

load_dotenv()

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Palmer Intelligence",
    description="Advanced AI-powered competitive intelligence platform with multi-site analysis, tech stack detection, and thought leadership content generation",
    version="2.0.0",
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

# Include routers
app.include_router(analysis.router, prefix="/api/v1", tags=["basic-analysis"])
app.include_router(competitive_analysis.router, prefix="/api/v1", tags=["competitive-intelligence"])

@app.get("/")
async def root():
    return {
        "message": "Palmer Intelligence API - Advanced Competitive Intelligence Platform",
        "version": "2.0.0",
        "status": "operational",
        "capabilities": {
            "multi_site_analysis": "Analyze up to 10 competitors simultaneously",
            "tech_stack_detection": "Identify CMS, frameworks, analytics, and more",
            "competitive_positioning": "Market leader vs challenger analysis",
            "viral_insights": "Generate LinkedIn-worthy thought leadership content",
            "industry_reports": "Create comprehensive industry analysis reports"
        },
        "endpoints": {
            "quick_scan": "/api/v1/quick-competitive-scan",
            "full_analysis": "/api/v1/competitive-analysis",
            "industry_report": "/api/v1/generate-industry-report",
            "api_docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "services": {
            "api": "operational",
            "competitive_intelligence": "ready",
            "tech_detection": "ready",
            "report_generation": "ready"
        }
    }
