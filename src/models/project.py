from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class ProjectBase(SQLModel):
    title: str = Field(..., title="Título del proyecto", max_length=100)
    description: str = Field(..., title="Descripción del proyecto", max_length=500)
    url: str = Field(..., title="URL del proyecto")
    repo_url: Optional[str] = Field(
        default=None, title="URL del repositorio del proyecto"
    )
    image: Optional[str] = Field(default=None, title="Imagen del proyecto")


class ProjectInternal(ProjectBase):
    id: Optional[int] = Field(default=None, primary_key=True)


class Project(ProjectInternal, table=True):
    __tablename__ = "projects"

    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ProjectCreate(ProjectBase):
    image: Optional[str] = Field(
        default="https://http.dog/404.jpg",
        title="Imagen del proyecto",
        description="URL de la imagen del proyecto. Debe ser una URL válida.",
    )


class ProjectUpdate(ProjectBase):
    title: Optional[str] = Field(
        default=None, title="Título del proyecto", max_length=100
    )
    description: Optional[str] = Field(
        default=None, title="Descripción del proyecto", max_length=500
    )
    url: Optional[str] = Field(default=None, title="URL del proyecto")
    repo_url: Optional[str] = Field(
        default=None, title="URL del repositorio del proyecto"
    )
    image: Optional[str] = Field(
        default="https://http.dog/404.jpg",
        title="Imagen del proyecto",
        description="URL de la imagen del proyecto. Debe ser una URL válida.",
    )


class ProjectRead(SQLModel):
    id: int
    title: str
    description: str
    url: str
    repo_url: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    image: Optional[str] = None
