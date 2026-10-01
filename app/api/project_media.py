import io
import uuid
from pathlib import Path

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile, status
from PIL import Image, UnidentifiedImageError
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.core.dependencies import get_current_user
from app.db.dependencies import get_db
from app.models.project import Project
from app.models.project_media import ProjectMedia
from app.models.user import User
from app.schemas.project_media import ProjectMediaResponse

router = APIRouter(prefix="/api/projects", tags=["Project Media"])


UPLOAD_DIR = Path("uploads/projects")
MAX_FILE_SIZE = 5 * 1024 * 1024
MAX_MEDIA_PER_PROJECT = 5
MAX_IMAGE_SIZE = 1600
ALLOWED_FORMATS = {"JPEG", "PNG", "WEBP"}


class ProjectMediaReorderRequest(BaseModel):
    media_ids: list[int]

@router.post(
    "/{project_id}/media",
    response_model=ProjectMediaResponse,
    status_code=status.HTTP_201_CREATED,
)
async def upload_project_media(
    project_id: int,
    file: UploadFile = File(...),
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.scalar(
        select(Project).where(
            Project.id == project_id,
            Project.owner_id == current_user.id,
        )
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    media_count = (
        db.scalar(
            select(func.count(ProjectMedia.id)).where(
                ProjectMedia.project_id == project_id
            )
        )
        or 0
    )

    if media_count >= MAX_MEDIA_PER_PROJECT:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A project can have at most 5 images",
        )

    contents = await file.read()

    if len(contents) > MAX_FILE_SIZE:
        raise HTTPException(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            detail="Image must be 5 MB or smaller",
        )

    try:
        image = Image.open(io.BytesIO(contents))
        image.load()
    except UnidentifiedImageError, OSError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid image file",
        )

    if image.format not in ALLOWED_FORMATS:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Only JPEG, PNG, and WebP images are allowed",
        )

    image.thumbnail((MAX_IMAGE_SIZE, MAX_IMAGE_SIZE))

    if image.mode not in ("RGB", "RGBA"):
        image = image.convert("RGBA")

    filename = f"{uuid.uuid4()}.webp"
    UPLOAD_DIR.mkdir(parents=True, exist_ok=True)

    output_path = UPLOAD_DIR / filename

    image.save(
        output_path,
        format="WEBP",
        quality=85,
    )

    position = media_count

    media = ProjectMedia(
        project_id=project_id,
        path=f"/uploads/projects/{filename}",
        alt=file.filename or "Project image",
        position=position,
    )

    db.add(media)
    db.commit()
    db.refresh(media)

    return media


@router.delete(
    "/{project_id}/media/{media_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project_media(
    project_id: int,
    media_id: int,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    media = db.scalar(
        select(ProjectMedia)
        .join(Project, Project.id == ProjectMedia.project_id)
        .where(
            ProjectMedia.id == media_id,
            ProjectMedia.project_id == project_id,
            Project.owner_id == current_user.id,
        )
    )

    if media is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Media not found",
        )

    file_path = Path(media.path.lstrip("/"))

    db.delete(media)
    db.commit()

    if file_path.exists():
        file_path.unlink()

    return None


@router.put(
    "/{project_id}/media/reorder",
    status_code=status.HTTP_204_NO_CONTENT,
)
def reorder_project_media(
    project_id: int,
    payload: ProjectMediaReorderRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = db.scalar(
        select(Project).where(
            Project.id == project_id,
            Project.owner_id == current_user.id,
        )
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    media = db.scalars(
        select(ProjectMedia).where(
            ProjectMedia.project_id == project_id
        )
    ).all()

    media_by_id = {item.id: item for item in media}

    if len(payload.media_ids) != len(media) or set(payload.media_ids) != set(media_by_id):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Media list does not match project media",
        )

    for position, media_id in enumerate(payload.media_ids):
        media_by_id[media_id].position = position

    db.commit()

    return None
