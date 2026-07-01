from typing import Optional
from pydantic import BaseModel , ConfigDict

class CategoryCreate(BaseModel):
    name:str
    description:str
    icon_url:Optional[str]=None

class CategoryUpdate(BaseModel):
    name:Optional[str]=None
    description : Optional[str]= None
    icon_url: Optional[str]=None 
    is_active: Optional[bool]=None

class CategoryResponse(BaseModel):
    id: int
    name: str
    description: str
    icon_url: Optional[str]
    is_active: bool

    model_config = ConfigDict(from_attributes=True)