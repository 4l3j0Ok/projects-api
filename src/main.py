import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import RedirectResponse
from fastapi.staticfiles import StaticFiles
from routers import projects
from core.config import AppConfig, PathConfig
from core.database import init_db
from core.logger import logger


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Maneja el ciclo de vida de la aplicación."""
    logger.info("Iniciando la API...")
    init_db()
    yield
    logger.info("Cerrando la API...")


app = FastAPI(
    title=AppConfig.APP_NAME,
    description=AppConfig.APP_DESCRIPTION,
    version=AppConfig.APP_VERSION,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=AppConfig.CORS_ALLOW_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(projects.router)

os.makedirs(PathConfig.IMAGES_DIR, exist_ok=True)
app.mount("/images", StaticFiles(directory=PathConfig.IMAGES_DIR), name="images")


@app.get("/")
def read_root():
    """Redirect to /docs"""
    return RedirectResponse(url="/docs")


if __name__ == "__main__":
    app.docs_url = "/docs" if AppConfig.DEV_MODE else None
    app.redoc_url = "/redoc" if AppConfig.DEV_MODE else None
    uvicorn.run(
        app="main:app",
        host=AppConfig.APP_HOST,
        port=AppConfig.APP_PORT,
        log_config=None,
        log_level=logger.level,
        reload=AppConfig.DEV_MODE,
    )
