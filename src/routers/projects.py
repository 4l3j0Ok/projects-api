from typing import Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlmodel import Session
from core.database import get_session
from services.projects import ProjectService
from models.project import ProjectCreate, ProjectRead

router = APIRouter(
    prefix="/projects",
    tags=["projects"],
)


@router.get("/", response_model=list[ProjectRead])
def get_projects(
    session: Session = Depends(get_session),
) -> list[ProjectRead]:
    return ProjectService.get_projects(session)


@router.post("/", response_model=ProjectRead, status_code=201)
async def create_project(
    title: str = Form(default="Proyecto"),
    description: str = Form(default="Descripción del proyecto"),
    url: str = Form(default="https://example.alejoide.com"),
    repo_url: Optional[str] = Form(default=None),
    image: Optional[UploadFile] = File(default=None),
    session: Session = Depends(get_session),
) -> ProjectRead:
    image_bytes = None
    if image:
        if not image.content_type or not image.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400, detail="El archivo debe ser una imagen válida."
            )
        image_bytes = await image.read()

    project_data = ProjectCreate(
        title=title, description=description, url=url, repo_url=repo_url
    )
    return ProjectService.create_project(project_data, image_bytes, session)
