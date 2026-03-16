import os
from typing import Generator
from sqlalchemy import inspect
from sqlmodel import Session, SQLModel, create_engine

from core.config import DatabaseConfig
from core.logger import logger

# Configuración específica para PostgreSQL
connect_args = {}

# Crear el engine de SQLModel
engine = create_engine(
    DatabaseConfig.DATABASE_URI,
    connect_args=connect_args,
    echo=True,
)


def is_first_time() -> bool:
    """Verificar si es la primera vez que se crea la base de datos."""
    return not inspect(engine).has_table("projects")


def create_db_and_tables(drop_existing: bool = False) -> None:
    """Crear la base de datos y todas las tablas."""
    if DatabaseConfig.TYPE == "sqlite":
        logger.info("Usando SQLite como base de datos.")
        db_dir = os.path.dirname(DatabaseConfig.SQLITE_DB_PATH)
        if not os.path.exists(db_dir):
            logger.info(f"Creando directorio para la base de datos en {db_dir}")
            os.makedirs(db_dir)
    if drop_existing:
        logger.warning("Eliminando todas las tablas existentes en la base de datos.")
        SQLModel.metadata.drop_all(engine)
    first_time = is_first_time()
    if first_time:
        logger.info("Creando todas las tablas en la base de datos.")
        SQLModel.metadata.create_all(engine)
    return


def get_session() -> Generator[Session, None, None]:
    """Dependencia para obtener una sesión de base de datos."""
    with Session(engine) as session:
        yield session


def init_db():
    """Inicializar la base de datos."""
    drop_db = os.getenv("CLEAR_DB_ON_STARTUP", "False").lower() == "true"
    create_db_and_tables(drop_existing=drop_db)
