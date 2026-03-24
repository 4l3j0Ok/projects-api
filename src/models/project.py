from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


class ProjectBase(SQLModel):
    title: str = Field(default="Proyecto", title="Título del proyecto", max_length=100)
    description: str = Field(
        default="Descripción del proyecto",
        title="Descripción del proyecto",
        max_length=500,
    )
    url: Optional[str] = Field(
        default="https://example.alejoide.com", title="URL del proyecto"
    )
    image: Optional[str] = Field(default=None, title="Imagen del proyecto")
    repo_url: Optional[str] = Field(
        default=None,
        title="URL del repositorio del proyecto",
    )


class ProjectInternal(ProjectBase):
    id: Optional[int] = Field(default=None, primary_key=True)


class Project(ProjectInternal, table=True):
    __tablename__ = "projects"

    active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=datetime.now)
    updated_at: datetime = Field(default_factory=datetime.now)


class ProjectCreate(ProjectBase):
    pass


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


class ProjectRead(ProjectBase):
    pass
