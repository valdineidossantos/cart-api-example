#from app.schemas.User_schemas import UserCreate, UserUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database_helper import db_session
from app.helpers.exceptions_helper import (GenericNotFoundException,
                                           UserNotFound)
from app.models.user_model import User
from app.repository.user_repository import UserRepository
from app.schemas.user_schemas import UserCreate, UserUpdate

router = APIRouter(
    prefix="/v1/users",
    tags=["users"]
)


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_users(db_session: AsyncSession = Depends(db_session)):
    user_repository = UserRepository(db_session, User)
    return await user_repository.get_all()


@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_user_by_id(user_id: int, db_session: AsyncSession = Depends(db_session)):
    user_repository = UserRepository(db_session, User)
    try:
        return await user_repository.get_by_id(user_id)
    except GenericNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(new_user: UserCreate, db_session: AsyncSession = Depends(db_session)):
    user_repository = UserRepository(db_session, User)
    user = User(
        name=new_user.name,
        email=new_user.email,
        active=new_user.active
    )
    print(f"\n Type:{type(new_user)} \n User: {user} \n")
    return await user_repository.create(user)


@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_User(user_id: int, db_session: AsyncSession = Depends(db_session)):
    user_repository = UserRepository(db_session, User)
    await user_repository.delete(user_id)
    return False


@router.put("/{user_id}", status_code=status.HTTP_200_OK)
async def update_User(update_user: UserUpdate, user_id: int, db_session: AsyncSession = Depends(db_session)):
    user_repository = UserRepository(db_session, User)

    user = User(
        name=update_user.name,
        email=update_user.email,
        active=update_user.active,
        id=user_id
    )
    try:
        return await user_repository.update(user)
    except GenericNotFoundException as error:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found")
