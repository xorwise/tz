from sqlalchemy import select
from core.database import Session
from models import Category
from schemas.category import CategoryRequest


async def create_category(db: Session, category: CategoryRequest) -> Category:
    new_category = Category(**category.model_dump())
    db.add(new_category)
    await db.commit()
    await db.refresh(new_category)
    return new_category


async def get_all_categories(db: Session, limit: int, offset: int) -> list[Category]:
    categories = await db.execute(select(Category).limit(limit).offset(offset))
    return list(categories.scalars().all())


async def get_category_by_id(db: Session, id: int) -> Category | None:
    category = await db.execute(select(Category).where(Category.id == id))
    return category.scalar()
