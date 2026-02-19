from fastapi import APIRouter

from src.api.v1.geolocation import router as geo_router

v1_router = APIRouter()
v1_router.include_router(geo_router, prefix="/geo", tags=["Geolocation"])
