from app.database.database_helper import Base
from sqlalchemy import Boolean, Column, Float, Integer, Numeric, String




class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=200), nullable=False)
    short_name = Column(String(length=100), nullable=False)
    description = Column(String(length=500))
    active = Column(Boolean, default=True)
    category = Column(String(length=100), nullable=False)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)
    quantity_stock = Column(Integer, nullable=False)
        


