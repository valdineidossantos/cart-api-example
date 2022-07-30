from typing import Union

from sqlalchemy import all_, and_, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.database.database_helper import Base
from app.helpers.exceptions_helper import GenericNotFoundException
from app.models.cart_model import Cart
from app.models.cupom_model import Cupom
from app.models.item_model import Item
from app.repository.base_repository import BaseRepository
from app.repository.item_repository import ItemRepository


class CartRepository(BaseRepository):
    def __init__(self, session: AsyncSession, model: Base):
        super().__init__(session, Cart)
        self.item_repository = ItemRepository(session, Item)

    async def create(self, cart: Cart) -> Union[Cart, None]:
        try:
            db_cart = await self.get_cart_by_user_id(cart.user_id)
            db_cart.cupoms_id = cart.cupoms_id
            self.session.add(db_cart)
            await self.session.commit()
            await self.session.refresh(db_cart)
            return db_cart
        except GenericNotFoundException:
            self.session.add(cart)
            await self.session.commit()
            return cart

    async def get_by_id(self, cart_id: int) -> Union[Base, None]:

        stmt = (
            select(self.model)
            .where(self.model.id == cart_id)
            .options(selectinload(Cart.items))
        )
        stream = await self.session.execute(stmt)
        result = stream.scalars().first()
        if result:
            return result

    async def update(self, cart: Cart) -> Union[Cart, None]:
        return await self.create_cart(cart)

    async def clean_cart(self, user_id: int) -> bool:
        result = await self.session.execute(
            select(self.model).where(self.model.user_id == user_id)
        )
        delete_cart = result.fetchone()

        # Cart found
        if delete_cart:
            delete_cart = delete_cart[0]
            await self.item_repository.delete_all_items_by_cart_id(delete_cart.id)
            await self.session.commit()
            await self.session.delete(delete_cart)
            await self.session.commit()
            return True

        # Object not found in database, delete not necessary
        return True

    async def get_cart_by_user_id(self, user_id: int) -> Union[Base, None]:
        try:
            stmt = (
                select(Cart)
                .join(Item, isouter=True)
                .join(Cupom, isouter=True)
                .where(Cart.user_id == user_id and Cart.finish_at is None)
                .options(selectinload(Cart.items), selectinload(Cart.cupoms))
            )
            stream = await self.session.execute(stmt)
            result = stream.scalars().first()
            if result:
                return result
            raise GenericNotFoundException(message="Cart not found")
        except NoResultFound:
            raise GenericNotFoundException(message="Cart not found")

    async def get_all(self) -> list:
        stmt = (
            select(Cart).where(Cart.finish_at is None).options(selectinload(Cart.items))
        )
        stream = await self.session.execute(stmt)
        return stream.scalars().all()
