from sqlalchemy import Boolean, Column, Float, Integer, String

from app.database.database_helper import Base


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

    def __repr__(self):
        return (
            "<Product(id='%s', name='%s', short_name='%s', description='%s', active='%s', category='%s', price='%s', in_stock='%s', quantity_stock='%s')>"
            % (
                self.id,
                self.name,
                self.short_name,
                self.description,
                self.active,
                self.category,
                self.price,
                self.in_stock,
                self.quantity_stock,
            )
        )
