from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class ProjectCreate(BaseModel):
    title: str = Field(min_length=1, max_length=150)
    tagline: str = Field(min_length=1, max_length=255)
    description_md: str = Field(min_length=1)
    tech: list[str] = Field(default_factory=list)
    github_url: HttpUrl | None = None
    demo_url: HttpUrl | None = None


class ProjectUpdate(BaseModel):
    title: str | None = Field(
        default=None,
        min_length=1,
        max_length=150,
    )
    tagline: str | None = Field(
        default=None,
        min_length=1,
        max_length=255,
    )
    description_md: str | None = Field(
        default=None,
        min_length=1,
    )
    tech: list[str] | None = None
    github_url: HttpUrl | None = None
    demo_url: HttpUrl | None = None


class ProjectResponse(BaseModel):
    id: int
    owner_id: int
    slug: str
    title: str
    tagline: str
    description_md: str
    tech: list[str]
    github_url: str | None
    demo_url: str | None
    is_published: bool
    view_count: int
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
