from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select, update
from sqlalchemy.orm import Session

from app.db.dependencies import get_db
from app.models.project import Project
from app.models.project_media import ProjectMedia
from app.models.user import User
from app.schemas.public import (
    PublicDeveloperResponse,
    PublicMediaResponse,
    PublicProjectPageResponse,
    PublicProjectResponse,
)

router = APIRouter(prefix="/api/public", tags=["Public"])


@router.get(
    "/dev/{username}",
    response_model=PublicDeveloperResponse,
)
def get_public_developer(
    username: str,
    db: Session = Depends(get_db),
):
    user = db.scalar(select(User).where(User.username == username.lower()))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Developer not found",
        )

    projects = db.scalars(
        select(Project)
        .where(
            Project.owner_id == user.id,
            Project.is_published.is_(True),
        )
        .order_by(Project.created_at.desc())
    ).all()

    project_responses = []

    for project in projects:
        media = db.scalars(
            select(ProjectMedia)
            .where(ProjectMedia.project_id == project.id)
            .order_by(ProjectMedia.position)
        ).all()

        project_responses.append(
            PublicProjectResponse(
                id=project.id,
                slug=project.slug,
                title=project.title,
                tagline=project.tagline,
                description_md=project.description_md,
                tech=project.tech,
                github_url=project.github_url,
                demo_url=project.demo_url,
                view_count=project.view_count,
                created_at=project.created_at,
                updated_at=project.updated_at,
                media=[PublicMediaResponse.model_validate(item) for item in media],
            )
        )

    return PublicDeveloperResponse(
        username=user.username,
        display_name=user.display_name,
        bio=user.bio,
        avatar_path=user.avatar_path,
        github_url=user.github_url,
        linkedin_url=user.linkedin_url,
        website_url=user.website_url,
        projects=project_responses,
    )


@router.get(
    "/dev/{username}/{slug}",
    response_model=PublicProjectPageResponse,
)
async def get_public_project(
    username: str,
    slug: str,
    db: Session = Depends(get_db),
):
    user = db.scalar(select(User).where(User.username == username.lower()))

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Developer not found",
        )

    project = db.scalar(
        select(Project).where(
            Project.owner_id == user.id,
            Project.slug == slug,
            Project.is_published.is_(True),
        )
    )

    if project is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Project not found",
        )

    db.execute(
        update(Project)
        .where(Project.id == project.id)
        .values(view_count=Project.view_count + 1)
    )
    db.commit()
    db.refresh(project)

    media = db.scalars(
        select(ProjectMedia)
        .where(ProjectMedia.project_id == project.id)
        .order_by(ProjectMedia.position)
    ).all()

    return PublicProjectPageResponse(
        developer={
            "username": user.username,
            "display_name": user.display_name,
            "avatar_path": user.avatar_path,
        },
        project=PublicProjectResponse(
            id=project.id,
            slug=project.slug,
            title=project.title,
            tagline=project.tagline,
            description_md=project.description_md,
            tech=project.tech,
            github_url=project.github_url,
            demo_url=project.demo_url,
            view_count=project.view_count,
            created_at=project.created_at,
            updated_at=project.updated_at,
            media=[PublicMediaResponse.model_validate(item) for item in media],
        ),
    )
