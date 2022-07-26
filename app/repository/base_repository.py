from typing import Union

from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database_helper import Base
from app.helpers.exceptions_helper import GenericNotFoundException


class BaseRepository:
    def __init__(self, session: AsyncSession, model: Base):
        self.session = session
        self.model = model
    
    async def get_all(self) -> list:
        result = await self.session.execute(select(self.model))
        return result.fetchall()
    
    async def get_by_id(self, requested_id: int) -> Union[Base, None]:
        try:
            result = await self.session.execute(select(self.model).where(self.model.id == requested_id))        
            return result.one()
        except NoResultFound as nrf:
            raise GenericNotFoundException(message=str(nrf))

            

    
    async def delete(self, requested_id: int) -> bool:
        result = await self.session.execute(select(self.model).where(self.model.id == requested_id))
        delete_item = result.fetchone()
        
        if delete_item:
                await self.session.delete(delete_item[0])
                await self.session.commit()
                return True
        
        #Object not found in database, delete not necessary
        return True
    
    
