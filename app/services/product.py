from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import selectinload
from core.database import Session
from models import Product
from schemas.product import ProductRequest
from utils.exceptions import IntegrityException


async def get_all_products(
    db: Session, limit: int, offset: int, **kwargs
) -> list[Product]:
    filters = {k: v for k, v in kwargs.items() if v is not None}
    products = await db.execute(
        select(Product)
        .options(selectinload(Product.category))
        .limit(limit)
        .offset(offset)
        .filter_by(**filters)
    )
    return list(products.scalars().all())


async def create_product(db: Session, product: ProductRequest) -> Product | Exception:
    new_product = Product(**product.model_dump())
    db.add(new_product)
    try:
        await db.commit()
    except IntegrityError:
        raise IntegrityException
    await db.refresh(new_product)
    await db.refresh(new_product, ["category"])
    return new_product


async def get_product_by_id(db: Session, id: int) -> Product | None:
    product = await db.execute(
        select(Product).where(Product.id == id).options(selectinload(Product.category))
    )
    return product.scalar()


async def update_product(
    db: Session, id: int, new_product: ProductRequest
) -> Product | None:
    product = await get_product_by_id(db, id)
    if not product:
        return None
    product.name = new_product.name
    product.description = new_product.description
    product.price = new_product.price
    product.quantity = new_product.quantity
    product.category_id = new_product.category_id
    try:
        await db.commit()
    except IntegrityError:
        raise IntegrityException
    await db.refresh(product)
    await db.refresh(product, ["category"])
    return product


async def delete_product(db: Session, product: Product) -> None:
    await db.delete(product)
    await db.commit()
