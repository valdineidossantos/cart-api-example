from typing import Union

from app.database.database_helper import Base
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository:
    def __init__(self, session: AsyncSession, model: Base):
        self.session = session
        self.model = model
    
    async def get_all(self) -> list:
        result = await self.session.execute(select(self.model))
        return result.fetchall()
    
    async def get_by_id(self, requested_id: int) -> Union[Base, None]:
        result = await self.session.execute(select(self.model).where(self.model.id == requested_id))        
        return result.one()

            

    
    async def delete(self, requested_id: int) -> bool:
        result = await self.session.execute(select(self.model).where(self.model.id == requested_id))
        delete_item = result.fetchone()
        
        if delete_item:
                await self.session.delete(delete_item[0])
                await self.session.commit()
                return True
        
        #Object not found in database, delete not necessary
        return True
    
    
