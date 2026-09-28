from pydantic import BaseModel, EmailStr, Field


class RegisterRequest(BaseModel):
    email: EmailStr
    username: str = Field(min_length=3, max_length=30)
    display_name: str = Field(min_length=1, max_length=100)
    password: str = Field(min_length=8)


class UserResponse(BaseModel):
    id: int
    email: str
    username: str
    display_name: str
