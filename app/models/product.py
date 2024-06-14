import sqlalchemy as sa
from sqlalchemy.orm import relationship
from core.database import Base


class Product(Base):
    __tablename__ = "products"

    id = sa.Column("id", sa.Integer, primary_key=True, index=True, autoincrement=True)
    name = sa.Column("name", sa.String(255), nullable=False, index=True)
    description = sa.Column("description", sa.TEXT, nullable=False)
    price = sa.Column("price", sa.Float(2), nullable=False)
    quantity = sa.Column("quantity", sa.Integer, nullable=False)
    category_id = sa.Column(
        "category_id", sa.Integer, sa.ForeignKey("categories.id", ondelete="CASCADE")
    )
    category = relationship("Category")
