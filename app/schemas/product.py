from pydantic import BaseModel
from .category import CategoryResponse


class ProductResponse(BaseModel):
    id: int
    name: str
    description: str
    price: float
    quantity: int
    category: CategoryResponse


class ProductRequest(BaseModel):
    name: str
    description: str
    price: float
    quantity: int
    category_id: int
