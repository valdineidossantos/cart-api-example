

from typing import Union

from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database_helper import Base
from app.helpers.exceptions_helper import UserNotFound
from app.models.user_model import User
from app.repository.base_repository import BaseRepository


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession, model: Base):
        super().__init__(session, model)
    
    async def create(self, user: User) -> Union[User, None]:       
        self.session.add(user)
        await self.session.commit()
        return user
    
    async def update(self, user: User) -> Union[User, None]:       

        try:
            database_user = await self.get_by_id(user.id)
            if database_user:
                database_user = database_user[0]
                database_user.name = user.name
                database_user.email = user.email
                database_user.active = user.active

                self.session.add(database_user)
                await self.session.commit()
                return database_user
        except NoResultFound:    
            raise UserNotFound("User not found")
