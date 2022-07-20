from app.database.database_helper import db_session
from app.helpers.exceptions_helper import GenericNotFoundException
from app.models.cart_model import Cart
from app.repository.cart_repository import CartRepository
from app.schemas.cart_schemas import CartCreate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(
    prefix="/v1/cart",
    tags=["cart"]
)



@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_carts( db_session: AsyncSession = Depends(db_session)):
    cart_repository = CartRepository (db_session, Cart)
    return await cart_repository.get_all()
    

@router.get("/{user_id}", status_code=status.HTTP_200_OK)
async def get_cart_by_user_id( user_id: int, db_session: AsyncSession = Depends(db_session)):
    cart_repository = CartRepository (db_session, Cart)
    try:
        return await cart_repository.get_cart_by_user_id(user_id)
    except GenericNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")



@router.post("/",  status_code=status.HTTP_201_CREATED)
async def create_cart( new_cart: CartCreate, db_session: AsyncSession = Depends(db_session)):
    cart_repository = CartRepository (db_session, Cart)
    user = Cart(
            user_id=new_cart.user_id
        )
    return await cart_repository.create(user)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def clear_user_cart( user_id: int, db_session: AsyncSession = Depends(db_session)):
    cart_repository = CartRepository (db_session, Cart)
    await cart_repository.clean_cart(user_id)
    return False

# @router.put("/{user_id}", status_code=status.HTTP_200_OK)
# async def update_User(update_user: UserUpdate, user_id: int, db_session: AsyncSession = Depends(db_session)):
#     cart_repository = CartRepository (db_session, User)
    
#     user = User(
#         name=update_user.name, 
#         email=update_user.email, 
#         active=update_user.active,
#         id=user_id

#     )
#     try:        
#         return await cart_repository.update(user)
#     except GenericNotFoundException as error:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")


