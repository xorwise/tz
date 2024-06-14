from pydantic import BaseModel


class CategoryResponse(BaseModel):
    id: int
    name: str


class CategoryRequest(BaseModel):
    name: str
