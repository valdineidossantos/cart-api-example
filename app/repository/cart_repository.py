

from typing import Union
from sqlalchemy import and_, select
from sqlalchemy.exc import NoResultFound    
from app.database.database_helper import Base
from app.helpers.exceptions_helper import GenericNotFoundException, UserNotFound
from app.models.cart_model import Cart

from app.repository.base_repository import BaseRepository
from sqlalchemy.ext.asyncio import AsyncSession


class CartRepository(BaseRepository):
    def __init__(self, session: AsyncSession, model: Base):
        super().__init__(session, model)
    
    async def create(self, cart: Cart) -> Union[Cart, None]:       
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
        delete_item = result.fetchone()
        #Cart found
        if delete_item:                
                await self.session.delete(delete_item[0])
                await self.session.commit()
                return True
        
        #Object not found in database, delete not necessary
        return True
    
    async def get_cart_by_user_id(self, user_id: int) -> Union[Base, None]:
        try:
            result = await self.session.execute(
                        select(self.model)
                            .where(
                                   and_( self.model.finish_at == None,
                                    self.model.user_id == user_id)
                                )
                                    
                                
                            )
            return result.one()
        except NoResultFound as nrf:
            raise GenericNotFoundException(message=str(nrf))
    
        
