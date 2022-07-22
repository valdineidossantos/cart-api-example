from secretstorage import Item
from app.database.database_helper import db_session
from app.helpers.exceptions_helper import GenericNotFoundException
from app.models.cart_model import Cart
from app.models.item_model import Item as ItemCart
from app.repository.cart_repository import CartRepository
from app.repository.item_repository import ItemRepository
from app.schemas.cart_schemas import CartCreate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.schemas.cart_schemas import CartSchemaResponse

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
        cart = await cart_repository.get_cart_by_user_id(user_id)
        return cart

    except GenericNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")



@router.post("/",  status_code=status.HTTP_201_CREATED)
async def create_cart( new_cart: CartCreate, db_session: AsyncSession = Depends(db_session)):
    cart_repository = CartRepository (db_session, Cart)
    item_repository = ItemRepository (db_session, ItemCart)
    cart = Cart(
            user_id=new_cart.user_id
        )
        
    database_cart = await cart_repository.create(cart)
    database_item = []
    await item_repository.delete_all_items_by_cart_id(database_cart.id)
    for item in new_cart.items:
        new_item = ItemCart()
        new_item.cart_id = database_cart.id
        new_item.product_id = item.product_id
        new_item.quantity = item.product_quantity
        new_item.cart = database_cart
        database_item.append(await item_repository.create(new_item))

    





@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def clear_user_cart( user_id: int, db_session: AsyncSession = Depends(db_session)):
    cart_repository = CartRepository (db_session, Cart)
    await cart_repository.clean_cart(user_id)
    return False

