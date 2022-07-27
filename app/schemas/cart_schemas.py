from typing import Union

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


class ItemSchemaResponse(BaseModel):

    product_id: int
    quantity: int


class CupomReponse(BaseModel):
    name: str
    discount: float
    active: bool

    class Config:
        orm_mode = True


class CartSchemaResponse(BaseModel):
    user_id: int
    cupoms: CupomReponse
    items: list[ItemSchemaResponse]

    class Config:
        orm_mode = True


class ItemSchemaResquestUpdate(BaseModel):
    product_id: int
    quantity: int

    @validator("quantity")
    def quantity_greatter_zero(cls, v):
        if v < 1:
            raise ValueError("Quantity must be greater than zero")
        return v

    class Config:
        orm_mode = True
