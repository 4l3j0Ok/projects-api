from dataclasses import dataclass
import os

from dotenv import load_dotenv
from pathlib import Path

load_dotenv()


@dataclass
class PathConfig:
    BASE_DIR = Path(__file__).parent.parent.resolve()
    DATA_DIR = BASE_DIR / "data"


@dataclass
class DatabaseConfig:
    TYPE = os.getenv("DB_TYPE", "sqlite").lower()
    SQLITE_DB_FILE_NAME = "projects.db"
    SQLITE_DB_PATH = os.getenv(
        "SQLITE_DB_PATH", str(PathConfig.DATA_DIR / SQLITE_DB_FILE_NAME)
    )
    DATABASE_URI = f"sqlite:///{SQLITE_DB_PATH}"


@dataclass
class AppConfig:
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT = int(os.getenv("APP_PORT", 8000))
    APP_NAME = "Gestión Digital API"
    APP_VERSION = os.getenv("APP_VERSION", "0.1.0")
    APP_DESCRIPTION = "API para la gestión de proyectos."
    DEV_MODE = os.getenv("DEV_MODE", "False").lower() == "true"
    CORS_ALLOW_ORIGINS = [
        origin.strip()
        for origin in os.getenv("CORS_ALLOW_ORIGINS", "*").split(",")
        if origin.strip()
    ]
    # Mantener esta lista ordenada alfabéticamente para
    # facilitar su lectura y mantenimiento
    INCLUDED_ROUTERS = ["projects"]


@dataclass
class LoggerConfig:
    LOG_NAME = os.getenv("LOG_NAME", "app")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
    LIBRARY_LOGS_PREFIXES = ("uvicorn", "fastapi", "sqlalchemy", "sqlmodel")
    LOG_COLORS = {
        "DEBUG": "blue",
        "INFO": "green",
        "WARNING": "yellow",
        "ERROR": "red",
        "CRITICAL": "bold_red",
    }
