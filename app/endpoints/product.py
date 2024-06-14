from fastapi import APIRouter, Depends, HTTPException
from core.database import get_session, Session
import services
from typing import Optional
from schemas.product import ProductResponse, ProductRequest
import services
from utils.exceptions import IntegrityException

product_router = APIRouter(
    prefix="/api/product",
    tags=["Product"],
)


@product_router.get("/", response_model=list[ProductResponse])
async def get_products(
    limit: int = 100,
    offset: int = 0,
    name: Optional[str] = None,
    description: Optional[str] = None,
    price: Optional[float] = None,
    quantity: Optional[int] = None,
    category_id: Optional[int] = None,
    db: Session = Depends(get_session),
):

    filters = {
        "name": name,
        "description": description,
        "price": price,
        "quantity": quantity,
        "category_id": category_id,
    }

    products = await services.get_all_products(db, limit, offset, **filters)
    return products


@product_router.post("/", response_model=ProductResponse, status_code=201)
async def create_product(product: ProductRequest, db: Session = Depends(get_session)):
    try:
        new_product = await services.create_product(db, product)
        return new_product
    except IntegrityException:
        raise HTTPException(status_code=400, detail="Specified category does not exist")


@product_router.get("/{id}", response_model=ProductResponse)
async def get_product(id: int, db: Session = Depends(get_session)):
    product = await services.get_product_by_id(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product


@product_router.put("/{id}", response_model=ProductResponse)
async def update_product(
    id: int, product: ProductRequest, db: Session = Depends(get_session)
):
    try:
        updated_product = await services.update_product(db, id, product)
        if not updated_product:
            raise HTTPException(status_code=404, detail="Product not found")
        return updated_product
    except IntegrityException:
        raise HTTPException(status_code=400, detail="Specified category does not exist")


@product_router.delete("/{id}", status_code=204)
async def delete_product(id: int, db: Session = Depends(get_session)):
    product = await services.get_product_by_id(db, id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    await services.delete_product(db, product)
