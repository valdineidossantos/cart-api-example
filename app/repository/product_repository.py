from typing import Union

from app.database.database_helper import Base
from app.helpers.exceptions_helper import ProductNotFound
from app.models.product_model import Product
from app.repository.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class ProductRepository(BaseRepository):
    def __init__(self, session: AsyncSession, model: Base):
        super().__init__(session, model)

    async def create(self, product: Product) -> Union[Product, None]:
        self.session.add(product)
        await self.session.commit()
        return product

    async def update(self, product: Product) -> Union[Product, None]:

        database_product = await self.get_by_id(product.id)

        if database_product:
            database_product = database_product[0]
            database_product.name = product.name
            database_product.short_name = product.short_name
            database_product.description = product.description
            database_product.category = product.category
            database_product.price = product.price
            database_product.in_stock = product.in_stock
            database_product.quantity_stock = product.quantity_stock

            self.session.add(database_product)
            await self.session.commit()
            return database_product

        raise ProductNotFound("Product not found")
