from typing import List

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.database.database_helper import db_session
from app.helpers.exceptions_helper import GenericNotFoundException
from app.mock_services.cupom_service import get_cupom_params_by_name
from app.models.cart_model import Cart
from app.models.item_model import Item as ItemCart
from app.repository.cart_repository import CartRepository
from app.repository.item_repository import ItemRepository
from app.schemas.cart_schemas import (CartCreate, CartSchemaResponse,
                                      ItemSchemaResquestUpdate)

router = APIRouter(
    prefix="/v1/cart",
    tags=["cart"]
)

@router.get("/{user_id}", status_code=status.HTTP_200_OK, response_model=CartSchemaResponse)
async def get_cart_by_user_id( user_id: int, db_session: AsyncSession = Depends(db_session)):
    cart_repository = CartRepository (db_session, Cart)
    try:
        cart = await cart_repository.get_cart_by_user_id(user_id)
        
        return_cart = {
            "user_id": cart.user_id,
            "cupoms": cart.cupoms,
            "items": [{"product_id":x.product_id, "quantity":x.quantity} for x in cart.items]
        }
        return return_cart
    except GenericNotFoundException:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")

@router.post("/",  status_code=status.HTTP_201_CREATED, response_model=None)
async def create_cart( new_cart: CartCreate, db_session: AsyncSession = Depends(db_session)):
    cart_repository = CartRepository (db_session, Cart)
    item_repository = ItemRepository (db_session, ItemCart)
    try:
        #Validate CUPOM 
        if new_cart.cupom: 
            db_cupom = await get_cupom_params_by_name(new_cart.cupom, db_session)
            
            if not db_cupom.active:                        
                raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cupom not valid")
            delattr(new_cart, 'cupom')
    except GenericNotFoundException:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Cupom not found")
    
    cupoms_id = db_cupom.id if db_cupom.id else None
    cart = Cart(
        user_id=new_cart.user_id,
        cupoms_id=cupoms_id
    )
    database_cart = await cart_repository.create(cart)

    database_item = []
    await item_repository.delete_all_items_by_cart_id(database_cart.id)
    for item in new_cart.items:
        new_item = ItemCart()
        new_item.cart_id = database_cart.id
        new_item.product_id = item.product_id
        new_item.quantity = item.quantity
        new_item.cart = database_cart
        database_item.append(await item_repository.create(new_item))

@router.put("/{cart_id}",  status_code=status.HTTP_200_OK, response_model=None)
async def update_cart(cart_id: int, new_cart: CartCreate, db_session: AsyncSession = Depends(db_session)):
    cart_repository = CartRepository (db_session, Cart)

    
    
    cart = await cart_repository.get_by_id(cart_id)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    
    return await create_cart(new_cart, db_session)


@router.post("/{cart_id}",  status_code=status.HTTP_200_OK, response_model=None)
async def add_product_in_cart(cart_id: int, item_cart: ItemSchemaResquestUpdate, db_session: AsyncSession = Depends(db_session)):
    cart_repository = CartRepository (db_session, Cart)
    cart = await cart_repository.get_by_id(cart_id)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")
    
    item_repository = ItemRepository (db_session, ItemCart)
    db_item = await item_repository.get_items_by_product_id(cart_id, item_cart.product_id)
    new_item = ItemCart()
    new_item.cart_id = cart_id
    new_item.product_id = item_cart.product_id
    new_item.quantity = item_cart.quantity
    result = await item_repository.create(new_item)   
    return result

@router.delete("/{cart_id}/{product_id}",  status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def delete_product_in_cart(cart_id: int, product_id: int, db_session: AsyncSession = Depends(db_session)):
    cart_repository = CartRepository (db_session, Cart)
    item_repository = ItemRepository (db_session, ItemCart)

    cart = await cart_repository.get_by_id(cart_id)
    if not cart:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found")

    await item_repository.delete_item(cart_id, product_id)

@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT, response_model=None)
async def clear_user_cart( user_id: int, db_session: AsyncSession = Depends(db_session)):
    cart_repository = CartRepository (db_session, Cart)
    await cart_repository.clean_cart(user_id)
    return False

