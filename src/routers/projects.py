from fastapi import APIRouter, Depends
from sqlmodel import Session
from core.database import get_session
from services.projects import ProjectService
from models.project import ProjectRead, ProjectCreate

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
def create_project(
    project: ProjectCreate,
    session: Session = Depends(get_session),
) -> ProjectRead:
    return ProjectService.create_project(project, session)
