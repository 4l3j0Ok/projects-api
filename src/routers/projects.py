from typing import Optional
from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from sqlmodel import Session
from core.database import get_session
from services.projects import ProjectService
from models.project import ProjectCreate, ProjectRead, ProjectUpdate

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
    title: str = Form(..., title="Título del proyecto", max_length=100),
    description: str = Form(..., title="Descripción del proyecto", max_length=500),
    url: str = Form(..., title="URL del proyecto"),
    repo_url: Optional[str] = Form(default=None),
    image: Optional[UploadFile] = File(default=None, title="Imagen del proyecto"),
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


@router.put("/{project_id}", response_model=ProjectRead)
async def update_project(
    project_id: int,
    title: Optional[str] = Form(
        default=None, title="Título del proyecto", max_length=100
    ),
    description: Optional[str] = Form(
        default=None, title="Descripción del proyecto", max_length=500
    ),
    url: Optional[str] = Form(default=None, title="URL del proyecto"),
    repo_url: Optional[str] = Form(default=None, title="URL del repositorio"),
    image: Optional[UploadFile] = File(default=None, title="Imagen del proyecto"),
    session: Session = Depends(get_session),
) -> ProjectRead:
    image_bytes = None
    if image:
        if not image.content_type or not image.content_type.startswith("image/"):
            raise HTTPException(
                status_code=400, detail="El archivo debe ser una imagen válida."
            )
        image_bytes = await image.read()

    project_data = ProjectUpdate(
        title=title,
        description=description,
        url=url,
        repo_url=repo_url,
    )
    return ProjectService.update_project(project_id, project_data, image_bytes, session)
