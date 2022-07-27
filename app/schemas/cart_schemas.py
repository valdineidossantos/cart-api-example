from typing import Any, Union

from pydantic import BaseModel, validator


class Items(BaseModel):
    product_id: int
    quantity: int

    @validator("quantity")
    def quantity_greatter_zero(cls, v):
        if v < 1:
            raise ValueError("Quantity must be greater than zero")
        return v

    class Config:
        orm_mode = True


class CartCreate(BaseModel):
    user_id: int
    cupom: Union[str, None] = None
    items: Union[list[Items], None] = None

    class Config:
        orm_mode = True


class CartUpdate(CartCreate):
    class Config:
        orm_mode = True


class ItemSchemaResquest(BaseModel):
    def __init__(self, product_id: int, quantity: int, cart_id: int):
        self.product_id = product_id
        self.quantity = quantity
        self.cart_id = cart_id

    product_id: int
    quantity: int

    @validator("quantity")
    def quantity_greatter_zero(cls, v):
        if v < 1:
            raise ValueError("Quantity must be greater than zero")
        return v


class CartSchemaResquest(BaseModel):
    id: int
    user_id: int
    finish_at: bool
    items: list[ItemSchemaResquest]


# Responses


class CupomReponse(BaseModel):
    name: str
    discount: float

    class Config:
        orm_mode = True


class ProductResponse(BaseModel):
    # id: int
    # active: bool
    name: str
    short_name: str
    price: float
    quantity_stock: int
    description: str
    category: str
    in_stock: bool

    class Config:
        orm_mode = True


class ItemSchemaResponse(BaseModel):
    product_id: int
    quantity: int
    product: ProductResponse


class CartSchemaResponse(BaseModel):
    user_id: int
    cupoms: Union[CupomReponse, None]
    items: list[Union[ItemSchemaResponse, None]]
    sub_total: Union[float, None]
    total: Union[float, None]
    discount: Union[float, None]

    class Config:
        orm_mode = True


class ItemSchemaResquestUpdate(BaseModel):
    product: ProductResponse
    quantity: int

    @validator("quantity")
    def quantity_greatter_zero(cls, v):
        if v < 1:
            raise ValueError("Quantity must be greater than zero")
        return v

    class Config:
        orm_mode = True
