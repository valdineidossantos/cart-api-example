from typing import Union

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database_helper import Base
from app.helpers.exceptions_helper import (DuplicatedItemException,
                                           GenericNotFoundException)
from app.models.cupom_model import Cupom
from app.repository.base_repository import BaseRepository


class CupomRepository(BaseRepository):
    def __init__(self, session: AsyncSession, model: Base):
        super().__init__(session, Cupom)

    async def create(self, cupom: Cupom) -> Union[Cupom, None]:
        cupom.name = cupom.name.upper()
        from sqlalchemy.exc import IntegrityError
        try:
            self.session.add(cupom)
            await self.session.commit()
            return cupom
        except (IntegrityError):
            self.session.rollback()
            raise DuplicatedItemException(
                message=f"Cupom already created [{cupom.name.upper()}]")

    async def update(self, cupom: Cupom) -> Union[Cupom, None]:
        stmt = select(self.model).where(self.model.id == cupom.id)
        stream = await self.session.execute(stmt)
        db_cupom = stream.scalars().first()

        if db_cupom:
            db_cupom.name = cupom.name.upper()
            db_cupom.discount = cupom.discount
            db_cupom.active = cupom.active
            try:
                self.session.add(db_cupom)
                await self.session.commit()
                return db_cupom
            except IntegrityError:
                self.session.rollback()
                raise DuplicatedItemException(
                    message=f"Cupom already created [{cupom.name.upper()}]")

        raise GenericNotFoundException(message="Cupom not found")

    async def get_cupom_by_name(self, name):
        stmt = select(self.model).where(self.model.name == name)
        stream = await self.session.execute(stmt)
        db_cupom = stream.scalars().first()
        if db_cupom:
            return db_cupom
        raise GenericNotFoundException(message="Cupom not found")

    async def get_all(self):
        stmt = select(self.model)
        stream = await self.session.execute(stmt)
        db_cupom = stream.scalars().all()
        if db_cupom:
            return db_cupom
        raise GenericNotFoundException(message="Cupom not found")
