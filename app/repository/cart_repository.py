

from sqlalchemy.orm import selectinload
from typing import Union
from sqlalchemy import all_, and_, func, select
from sqlalchemy.exc import NoResultFound    
from app.database.database_helper import Base
from app.helpers.exceptions_helper import GenericNotFoundException, UserNotFound
from app.models.cart_model import Cart
from app.models.item_model import Item

from app.repository.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession

from app.repository.item_repository import ItemRepository
from app.schemas.cart_schemas import CartSchemaResquest, ItemSchemaResquest


class CartRepository(BaseRepository):
    def __init__(self, session: AsyncSession, model: Base):
        super().__init__(session, model)
        self.item_repository = ItemRepository(session, Item)
    
    async def create(self, cart: Cart) -> Union[Cart, None]:       
        try:
            valid_exists = await self.get_cart_by_user_id(cart.user_id)        
            return valid_exists
        except GenericNotFoundException:
            self.session.add(cart)
            await self.session.commit()
            return cart
        

    
    async def update(self, cart: Cart) -> Union[Cart, None]:       

        try:
            database_cart = await self.get_by_id(cart.id)
            if database_cart:
                database_cart = database_cart[0]
                database_cart.user_id = cart.user_id
                database_cart.finish_at = cart.finish_at
                self.session.add(database_cart)
                await self.session.commit()
                return database_cart
        except NoResultFound:    
            raise GenericNotFoundException("Cart not found")
    
    
    async def clean_cart(self, user_id: int) -> bool:
        result = await self.session.execute(select(self.model).where(self.model.user_id == user_id))
        delete_cart = result.fetchone() 

        #Cart found
        if delete_cart:   
                delete_cart = delete_cart[0]
                await self.item_repository.delete_all_items_by_cart_id(delete_cart.id)
                await self.session.commit()
                await self.session.delete(delete_cart)
                await self.session.commit()
                return True
        
        #Object not found in database, delete not necessary
        return True

    async def get_cart_by_user_id(self, user_id: int) -> Union[Base, None]:
        
        stmt = select(Cart).where(
                                   and_(
                                    Cart.finish_at == None,
                                    Cart.user_id == user_id, 
                                    )
                                ).options(selectinload(Cart.items))
        
        stream =  await self.session.execute(stmt)
        result = stream.scalars().first()
        if result:
            return result
        raise GenericNotFoundException(message="Cart not found")
        
    
    async def get_all(self) -> list:
        stmt = select(Cart).where(
                                 Cart.finish_at == None
                                ).options(selectinload(Cart.items))
        stream =  await self.session.execute(stmt)
        return  stream.scalars().all()
        
        
        
        
