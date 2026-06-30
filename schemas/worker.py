from typing import Optional
from pydantic import BaseModel, ConfigDict


class WorkerCreate(BaseModel):
    bio: str
    experience_summary: str
    location_city: str
    location_state: str


class WorkerUpdate(BaseModel):
    bio: Optional[str] = None
    experience_summary: Optional[str] = None
    location_city: Optional[str] = None
    location_state: Optional[str] = None


class WorkerResponse(BaseModel):
    id: int
    bio: str
    experience_summary: str
    location_city: str
    location_state: str
    rating_avg: float
    rating_count: int
    is_verified: bool

    model_config = ConfigDict(from_attributes=True)