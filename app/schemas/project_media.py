from pydantic import BaseModel, ConfigDict


class ProjectMediaResponse(BaseModel):
    id: int
    project_id: int
    path: str
    alt: str
    position: int

    model_config = ConfigDict(from_attributes=True)
