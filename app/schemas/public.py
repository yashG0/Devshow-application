from datetime import datetime

from pydantic import BaseModel, ConfigDict


class PublicMediaResponse(BaseModel):
    id: int
    path: str
    alt: str
    position: int

    model_config = ConfigDict(from_attributes=True)


class PublicProjectResponse(BaseModel):
    id: int
    slug: str
    title: str
    tagline: str
    description_md: str
    tech: list[str]
    github_url: str | None
    demo_url: str | None
    view_count: int
    created_at: datetime
    updated_at: datetime
    media: list[PublicMediaResponse]


class PublicDeveloperResponse(BaseModel):
    username: str
    display_name: str
    bio: str | None
    avatar_path: str | None
    github_url: str | None
    linkedin_url: str | None
    website_url: str | None
    projects: list[PublicProjectResponse]
