from sqlmodel import Session, select

from models.project import Project, ProjectCreate


class ProjectService:
    @staticmethod
    def get_projects(session: Session) -> list[Project | None]:
        statement = select(Project)
        results = session.exec(statement).all()
        return results

    @staticmethod
    def create_project(project: ProjectCreate, session: Session) -> Project:

        db_project = Project.model_validate(project)
        session.add(db_project)
        session.commit()
        session.refresh(db_project)  # Refresca el objeto para obtener el ID generado
        return db_project
