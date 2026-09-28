from pydantic import BaseModel, ConfigDict, Field, HttpUrl


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    display_name: str
    bio: str | None
    avatar_path: str | None
    github_url: str | None
    linkedin_url: str | None
    website_url: str | None

    model_config = ConfigDict(from_attributes=True)


class UserUpdate(BaseModel):
    display_name: str | None = Field(
        default=None,
        min_length=1,
        max_length=100,
    )
    bio: str | None = Field(
        default=None,
        max_length=1000,
    )
    github_url: HttpUrl | None = None
    linkedin_url: HttpUrl | None = None
    website_url: HttpUrl | None = None
