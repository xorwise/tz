from fastapi import APIRouter, Depends, HTTPException
from core.database import get_session, Session
import services

from schemas.category import CategoryResponse, CategoryRequest
import services

category_router = APIRouter(
    prefix="/api/category",
    tags=["Category"],
)


@category_router.get("/", response_model=list[CategoryResponse])
async def get_categories(
    limit: int = 100, offset: int = 0, db: Session = Depends(get_session)
):
    categories = await services.get_all_categories(db, limit, offset)
    return categories


@category_router.post("/", response_model=CategoryResponse, status_code=201)
async def create_category(
    category: CategoryRequest, db: Session = Depends(get_session)
):
    new_category = await services.create_category(db, category)
    return new_category


@category_router.get("/{id}", response_model=CategoryResponse)
async def get_category(id: int, db: Session = Depends(get_session)):
    category = await services.get_category_by_id(db, id)
    if not category:
        raise HTTPException(status_code=404, detail="Category not found")
    return category
