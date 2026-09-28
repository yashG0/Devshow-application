import re

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models.project import Project


def generate_slug(
    title: str,
    owner_id: int,
    db: Session,
) -> str:
    slug = re.sub(r"[^a-z0-9]+", "-", title.lower()).strip("-")

    if not slug:
        slug = "project"

    base_slug = slug
    counter = 2

    while db.scalar(
        select(Project).where(
            Project.owner_id == owner_id,
            Project.slug == slug,
        )
    ):
        slug = f"{base_slug}-{counter}"
        counter += 1

    return slug
