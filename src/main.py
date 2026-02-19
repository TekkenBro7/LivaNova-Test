import uvicorn
from fastapi import FastAPI

from src.api.router import api_router
from src.core.config import base_config
from src.core.constants import DESCRIPTION

app = FastAPI(
    title=base_config.APP_NAME,
    version="1.0.0",
    description=DESCRIPTION,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json",
)

app.include_router(api_router, prefix="/api")

if __name__ == "__main__":
    uvicorn.run(
        "src.main:app",
        host=base_config.HOST,
        port=base_config.PORT,
        reload=base_config.RELOAD,
    )
