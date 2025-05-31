from fastapi import APIRouter
from .endpoints import analysis, competitive, intelligence, auth, health

api_router = APIRouter()

api_router.include_router(auth.router, prefix="/auth", tags=["authentication"])
api_router.include_router(analysis.router, prefix="/analysis", tags=["analysis"])
api_router.include_router(competitive.router, prefix="/competitive", tags=["competitive"])
api_router.include_router(intelligence.router, prefix="/intelligence", tags=["intelligence"])
api_router.include_router(health.router, prefix="/health", tags=["health"])
