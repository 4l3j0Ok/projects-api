import os
import uuid
from datetime import datetime
from io import BytesIO
from typing import Optional

from fastapi import HTTPException
from PIL import Image
from sqlmodel import Session, select

from core.config import AppConfig, PathConfig
from models.project import Project, ProjectCreate, ProjectUpdate


class ProjectService:
    @staticmethod
    def _ensure_images_directory():
        os.makedirs(PathConfig.IMAGES_DIR, exist_ok=True)

    @staticmethod
    def _save_image_to_file(image_bytes: bytes, project_id: int) -> str:
        """Guarda la imagen en el sistema de archivos como WebP y retorna el nombre del archivo."""
        ProjectService._ensure_images_directory()

        img = Image.open(BytesIO(image_bytes))

        if img.mode in ("RGBA", "LA", "P"):
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(
                img, mask=img.split()[-1] if img.mode in ("RGBA", "LA") else None
            )
            img = background
        elif img.mode != "RGB":
            img = img.convert("RGB")

        filename = f"{project_id}_{uuid.uuid4().hex[:8]}.webp"
        filepath = os.path.join(PathConfig.IMAGES_DIR, filename)
        img.save(filepath, format="WEBP", quality=85, method=6)

        return filename

    @staticmethod
    def _delete_image_file(filename: str):
        filepath = os.path.join(PathConfig.IMAGES_DIR, filename)
        if os.path.exists(filepath):
            try:
                os.remove(filepath)
            except Exception as e:
                print(f"Error al eliminar imagen {filename}: {e}")

    @staticmethod
    def _is_local_image(image: str) -> bool:
        return not image.startswith("http://") and not image.startswith("https://")

    @staticmethod
    def _image_to_url(image: str) -> str:
        """Convierte un nombre de archivo local a URL completa."""
        if ProjectService._is_local_image(image):
            return f"{AppConfig.IMAGES_BASE_URL}/{image}"
        return image

    @staticmethod
    def get_projects(session: Session) -> list[Project | None]:
        statement = select(Project)
        results = session.exec(statement).all()
        for project in results:
            if project.image:
                project.image = ProjectService._image_to_url(project.image)
        return results

    @staticmethod
    def create_project(
        project: ProjectCreate, image_bytes: Optional[bytes], session: Session
    ) -> Project:
        db_project = Project.model_validate(project)
        session.add(db_project)
        session.commit()
        session.refresh(db_project)

        if image_bytes:
            try:
                filename = ProjectService._save_image_to_file(
                    image_bytes, db_project.id
                )
            except Exception as e:
                raise HTTPException(
                    status_code=400, detail=f"Error al procesar la imagen: {str(e)}"
                )
            db_project.image = filename
            session.add(db_project)
            session.commit()
            session.refresh(db_project)

        if db_project.image:
            db_project.image = ProjectService._image_to_url(db_project.image)

        return db_project

    @staticmethod
    def update_project(
        project_id: int,
        project: ProjectUpdate,
        image_bytes: Optional[bytes],
        session: Session,
    ) -> Project:
        db_project = session.get(Project, project_id)
        if not db_project:
            raise HTTPException(status_code=404, detail="Proyecto no encontrado")

        update_data = project.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_project, key, value)

        if image_bytes:
            try:
                filename = ProjectService._save_image_to_file(
                    image_bytes, db_project.id
                )
            except Exception as e:
                raise HTTPException(
                    status_code=400, detail=f"Error al procesar la imagen: {str(e)}"
                )

            if db_project.image and ProjectService._is_local_image(db_project.image):
                ProjectService._delete_image_file(db_project.image)

            db_project.image = filename

        db_project.updated_at = datetime.now()
        session.add(db_project)
        session.commit()
        session.refresh(db_project)

        if db_project.image:
            db_project.image = ProjectService._image_to_url(db_project.image)

        return db_project
