import sqlalchemy as sa
from core.database import Base


class Category(Base):
    __tablename__ = "categories"

    id = sa.Column("id", sa.Integer, primary_key=True, index=True, autoincrement=True)
    name = sa.Column("name", sa.String(255), nullable=False, index=True)
