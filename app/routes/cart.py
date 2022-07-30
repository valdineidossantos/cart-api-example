from typing import List

from app.database.database_helper import db_session
from app.helpers.exceptions_helper import CupomException, GenericNotFoundException
from app.mock_services.cupom_service import get_cupom_params_by_name
from app.mock_services.product_service import get_product_params_by_id
from app.models.cart_model import Cart
from app.models.item_model import Item as ItemCart
from app.repository.cart_repository import CartRepository
from app.repository.item_repository import ItemRepository
from app.schemas.cart_schemas import (
    CartCreate,
    CartSchemaResponse,
    ItemSchemaRequestUpdate,
)
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/v1/cart", tags=["cart"])


@router.get(
    "/{user_id}",
    status_code=status.HTTP_200_OK,
    response_model=CartSchemaResponse,
    summary="Request User Cart",
    description="Request User Cart based on user identification",
)
async def get_cart_by_user_id(
    user_id: int, db_session: AsyncSession = Depends(db_session)
):
    cart_repository = CartRepository(db_session, Cart)
    try:

        cart = await cart_repository.get_cart_by_user_id(user_id)

        return_cart = {
            "user_id": cart.user_id,
            "cupoms": cart.cupoms,
            "items": [
                {"product_id": x.product_id, "quantity": x.quantity} for x in cart.items
            ],
        }

        return_cart["items"] = await get_last_product_params(
            db_session, return_cart["items"]
        )

        return_cart["sub_total"] = sum(
            [x["product"].price * x["quantity"] for x in return_cart["items"]]
        )

        if cart.cupoms:
            cupom = await get_cupom_params_by_name(cart.cupoms.name, db_session)
            return_cart["discount"] = cupom.discount
            applied_discount = return_cart["sub_total"] - cupom.discount
            return_cart["total"] = applied_discount if applied_discount > 0 else 0
        else:
            return_cart["total"] = return_cart["sub_total"]
        return return_cart
    except GenericNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )


async def get_last_product_params(db_session, items):
    all_products = []
    for item in items:
        product = dict(await get_product_params_by_id(item["product_id"], db_session))
        product["product_id"] = product.get("Product").id
        product["quantity"] = item["quantity"]
        product["product"] = product.get("Product")
        del product["Product"]
        all_products.append(product)

    return all_products


@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=None,
    summary="Create a User Cart",
    description="Create a User Cart sended by body",
)
async def create_cart(
    new_cart: CartCreate, db_session: AsyncSession = Depends(db_session)
):
    cart_repository = CartRepository(db_session, Cart)
    item_repository = ItemRepository(db_session, ItemCart)

    cart = Cart(user_id=new_cart.user_id)
    try:
        cupom = await cart.validate_cupom_and_apply(new_cart.cupom, db_session)
    except GenericNotFoundException as ge:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(ge))
    except CupomException as ce:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(ce))

    product_errors = await cart.validate_items(new_cart.items, db_session)

    if product_errors:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail=product_errors
        )

    database_cart = await cart_repository.create(cart)
    database_cart.cupoms = cupom
    database_cart.cupoms_id = cupom.id if cupom else None

    database_item = []
    await item_repository.delete_all_items_by_cart_id(database_cart.id)
    for item in new_cart.items:
        new_item = ItemCart()
        new_item.cart_id = database_cart.id
        new_item.product_id = item.product_id
        new_item.quantity = item.quantity
        new_item.cart = database_cart
        database_item.append(await item_repository.create(new_item))

    await db_session.flush()


@router.put(
    "/{cart_id}",
    status_code=status.HTTP_200_OK,
    response_model=None,
    summary="Update a Cart",
    description="Update a Cart based in cart identification sended update data by body",
)
async def update_cart(
    cart_id: int, new_cart: CartCreate, db_session: AsyncSession = Depends(db_session)
):
    cart_repository = CartRepository(db_session, Cart)

    cart = await cart_repository.get_by_id(cart_id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )

    return await create_cart(new_cart, db_session)


@router.post(
    "/{cart_id}",
    status_code=status.HTTP_200_OK,
    response_model=None,
    summary="Adding a product in Cart",
    description="Update a Cart based in cart identification sended update data by body",
)
async def add_product_in_cart(
    cart_id: int,
    item_cart: ItemSchemaRequestUpdate,
    db_session: AsyncSession = Depends(db_session),
):
    cart_repository = CartRepository(db_session, Cart)
    cart = await cart_repository.get_by_id(cart_id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )

    item_repository = ItemRepository(db_session, ItemCart)
    db_item = await item_repository.get_items_by_product_id(
        cart_id, item_cart.product_id
    )
    new_item = ItemCart()
    new_item.cart_id = cart_id
    new_item.product_id = item_cart.product_id
    new_item.quantity = item_cart.quantity
    result = await item_repository.create(new_item)
    return result


@router.delete(
    "/{cart_id}/{product_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    summary="Delete a product in Cart",
    description="Delete the product in Cart based in cart identification and product identification",
)
async def delete_product_in_cart(
    cart_id: int, product_id: int, db_session: AsyncSession = Depends(db_session)
):
    cart_repository = CartRepository(db_session, Cart)
    item_repository = ItemRepository(db_session, ItemCart)

    cart = await cart_repository.get_by_id(cart_id)
    if not cart:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Cart not found"
        )

    await item_repository.delete_item(cart_id, product_id)


@router.delete(
    "/{user_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_model=None,
    summary="Delete a Cart",
    description="Delete a user cart and delete all product in this Cart",
)
async def clear_user_cart(user_id: int, db_session: AsyncSession = Depends(db_session)):
    cart_repository = CartRepository(db_session, Cart)
    await cart_repository.clean_cart(user_id)
    return False
