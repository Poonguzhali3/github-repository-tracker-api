from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class RepositoryBase(BaseModel):
    owner: str = Field(..., example="tiangolo")
    repo_name: str = Field(..., example="fastapi")


class RepositoryCreate(RepositoryBase):
    pass


class RepositoryUpdate(BaseModel):
    stars: Optional[int] = Field(None, ge=0)
    language: Optional[str] = None
    description: Optional[str] = None


class RepositoryResponse(RepositoryBase):
    id: int
    stars: int
    language: Optional[str]
    description: Optional[str]
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True
