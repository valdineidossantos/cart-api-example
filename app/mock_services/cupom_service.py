from sqlalchemy.ext.asyncio import AsyncSession

from app.models.cupom_model import Cupom
from app.repository.cupom_repository import CupomRepository
from app.helpers.exceptions_helper import GenericNotFoundException

def get_cupom_params_by_name(name:str, db_session: AsyncSession) -> Cupom:
    cupom_repository = CupomRepository (db_session, Cupom)

    cupom = cupom_repository.get_cupom_by_name(name)
    
    if cupom:
        return cupom
    
    raise GenericNotFoundException(message="Cupom not found")