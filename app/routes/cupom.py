from fastapi import APIRouter, Depends, HTTPException, status
from secretstorage import Item
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database_helper import db_session
from app.helpers.exceptions_helper import (DuplicatedItemException,
                                           GenericNotFoundException)
from app.models.cupom_model import Cupom
from app.repository.cupom_repository import CupomRepository
from app.schemas.cupom_schemas import CupomRequest

router = APIRouter(prefix="/v1/cupom", tags=["cupom"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_cumpoms(db_session: AsyncSession = Depends(db_session)):
    cupom_repository = CupomRepository(db_session, Cupom)
    try:
        cupom = await cupom_repository.get_all()
        return cupom

    except GenericNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cupom not found"
        )


@router.get("/by-id/{cupom_id}", status_code=status.HTTP_200_OK)
async def get_cumpom_by_id(
    cupom_id: int, db_session: AsyncSession = Depends(db_session)
):
    cupom_repository = CupomRepository(db_session, Cupom)
    try:
        cupom = await cupom_repository.get_by_id(cupom_id)
        return cupom

    except GenericNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cupom not found"
        )


@router.get("/by-name/{cupom}", status_code=status.HTTP_200_OK)
async def get_cumpom_by_name(
    cupom: str, db_session: AsyncSession = Depends(db_session)
):
    cupom_repository = CupomRepository(db_session, Cupom)
    try:
        cupom = await cupom_repository.get_cupom_by_name(cupom)
        return cupom

    except GenericNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cupom not found"
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_cupom(
    new_cupom: CupomRequest, db_session: AsyncSession = Depends(db_session)
):
    cupom_repository = CupomRepository(db_session, Cupom)

    cupom = Cupom(**new_cupom.dict())
    try:
        database_cupom = await cupom_repository.create(cupom)
        return database_cupom
    except DuplicatedItemException as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=f"{str(error)}"
        )


@router.put("/{cupom_id}", status_code=status.HTTP_200_OK)
async def update_cupom(
    cupom_id: int,
    new_cupom: CupomRequest,
    db_session: AsyncSession = Depends(db_session),
):
    cupom_repository = CupomRepository(db_session, Cupom)
    try:

        cupom = Cupom(**new_cupom.dict())
        cupom.id = cupom_id

        return await cupom_repository.update(cupom)

    except GenericNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cupom not found"
        )


@router.delete("/{cupom_id}", status_code=status.HTTP_200_OK)
async def delete_cupom(cupom_id: int, db_session: AsyncSession = Depends(db_session)):
    cupom_repository = CupomRepository(db_session, Cupom)
    try:
        return await cupom_repository.delete(cupom_id)

    except GenericNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cupom not found"
        )
