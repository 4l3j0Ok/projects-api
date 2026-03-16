import uvicorn
from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from routers import projects
from core.config import AppConfig
from core.database import init_db
from core.logger import logger
from contextlib import asynccontextmanager


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

app.include_router(projects.router)


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
