from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.core.dependencies import get_current_user
from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.user import UserResponse, UserUpdate

router = APIRouter(prefix="/api", tags=["User"])


@router.get("/me", response_model=UserResponse)
def get_me(
    current_user: User = Depends(get_current_user),
):
    return current_user


@router.patch("/me", response_model=UserResponse)
def update_me(
    data: UserUpdate,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if data.display_name is not None:
        current_user.display_name = data.display_name

    if data.bio is not None:
        current_user.bio = data.bio

    if data.github_url is not None:
        current_user.github_url = data.github_url

    if data.linkedin_url is not None:
        current_user.linkedin_url = data.linkedin_url

    if data.website_url is not None:
        current_user.website_url = data.website_url

    db.commit()
    db.refresh(current_user)

    return current_user
