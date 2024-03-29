from typing import Union

from sqlalchemy import and_, delete, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database_helper import Base
from app.helpers.exceptions_helper import GenericNotFoundException
from app.models.item_model import Item
from app.repository.base_repository import BaseRepository


class ItemRepository(BaseRepository):
    def __init__(self, session: AsyncSession, model: Base):
        super().__init__(session, model)

    async def create(self, item: Item) -> Union[Item, None]:

        database_items = await self.get_all_items_by_cart_id(item.cart_id)

        for data_base_item in database_items:
            data_base_item = data_base_item[0]
            # Add and update products
            if data_base_item.product_id == item.product_id:
                data_base_item.quantity = item.quantity
                self.session.add(data_base_item)
                await self.session.commit()
                return item
        self.session.add(item)
        await self.session.commit()
        return item

    async def delete_all_items_by_cart_id(self, cart_id):
        await self.session.execute(
            delete(self.model).where(self.model.cart_id == cart_id)
        )
        await self.session.commit()

    async def delete_item(self, cart_id, product_id):
        stmt = delete(self.model).where(
            and_(self.model.cart_id == cart_id, product_id == self.model.product_id)
        )
        await self.session.execute(stmt)
        self.session.commit()

    async def create_all(self, items: list[Item]) -> Union[list[Item], None]:
        self.session.add_all(items)
        await self.session.commit()
        return items

    async def get_all_items_by_cart_id(self, cart_id: int) -> Union[Base, None]:
        result = await self.session.execute(
            select(self.model, Item).where(self.model.cart_id == cart_id)
        )
        return result.all()

    async def get_items_by_product_id(
        self, cart_id: int, product_id: int
    ) -> Union[Base, None]:
        stmt = select(self.model, Item).where(
            and_(self.model.product_id == product_id, self.model.cart_id == cart_id)
        )

        result = await self.session.execute(stmt)

        return result.first()
