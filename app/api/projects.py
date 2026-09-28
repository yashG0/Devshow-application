from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.dependencies import get_db
from app.models.project import Project
from app.models.project_media import ProjectMedia
from app.models.user import User
from app.schemas.project import (
    ProjectCreate,
    ProjectMediaResponse,
    ProjectResponse,
    ProjectUpdate,
)
from app.services.project import generate_slug

router = APIRouter(
    prefix="/api/projects",
    tags=["Projects"],
)


@router.post(
    "",
    response_model=ProjectResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_project(
    data: ProjectCreate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    project = Project(
        owner_id=current_user.id,
        slug=generate_slug(
            data.title,
            current_user.id,
            db,
        ),
        title=data.title,
        tagline=data.tagline,
        description_md=data.description_md,
        tech=data.tech,
        github_url=str(data.github_url) if data.github_url else None,
        demo_url=str(data.demo_url) if data.demo_url else None,
    )

    db.add(project)
    db.commit()
    db.refresh(project)

    return build_project_response(project, db)


@router.get(
    "",
    response_model=list[ProjectResponse],
)
def list_my_projects(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    return db.scalars(
        select(Project)
        .where(Project.owner_id == current_user.id)
        .order_by(Project.created_at.desc())
    ).all()


@router.get(
    "/{project_id}",
    response_model=ProjectResponse,
)
def get_project(
    project_id: int,
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

    return build_project_response(project, db)


@router.patch(
    "/{project_id}",
    response_model=ProjectResponse,
)
def update_project(
    project_id: int,
    data: ProjectUpdate,
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

    updates = data.model_dump(exclude_unset=True)

    for field, value in updates.items():
        if field in {"github_url", "demo_url"} and value is not None:
            value = str(value)

        setattr(project, field, value)

    db.commit()
    db.refresh(project)

    return build_project_response(project, db)


@router.delete(
    "/{project_id}",
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_project(
    project_id: int,
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

    db.delete(project)
    db.commit()


@router.patch(
    "/{project_id}/publish",
    response_model=ProjectResponse,
)
def toggle_publish(
    project_id: int,
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

    project.is_published = not project.is_published

    db.commit()
    db.refresh(project)

    return build_project_response(project, db)


def build_project_response(
    project: Project,
    db: Session,
) -> ProjectResponse:
    media = db.scalars(
        select(ProjectMedia)
        .where(ProjectMedia.project_id == project.id)
        .order_by(ProjectMedia.position)
    ).all()

    return ProjectResponse(
        id=project.id,
        owner_id=project.owner_id,
        slug=project.slug,
        title=project.title,
        tagline=project.tagline,
        description_md=project.description_md,
        tech=project.tech,
        github_url=project.github_url,
        demo_url=project.demo_url,
        is_published=project.is_published,
        view_count=project.view_count,
        created_at=project.created_at,
        updated_at=project.updated_at,
        media=[ProjectMediaResponse.model_validate(item) for item in media],
    )
