import datetime
from enum import Enum
from typing import Union
from pydantic import BaseModel, validator


class Items(BaseModel):
    product_id: int
    quantity: int
    @validator('quantity')
    def quantity_greatter_zero(cls, v):
        if v < 1:
            raise ValueError('Quantity must be greater than zero')
        return v


    class Config:
        orm_mode = True

class CartCreate(BaseModel):
    user_id: int
    items: Union[list[Items], None] = None
    
    class Config:
        orm_mode = True

class CartUpdate(CartCreate):

    class Config:
        orm_mode = True


class ItemSchemaResquest (BaseModel):
    def __init__(self, product_id: int, quantity: int, cart_id: int):
        self.product_id = product_id
        self.quantity = quantity
        self.cart_id = cart_id
    product_id: int
    quantity: int

    @validator('quantity')
    def quantity_greatter_zero(cls, v):
        if v < 1:
            raise ValueError('Quantity must be greater than zero')
        return v    

class CartSchemaResquest(BaseModel):
    id: int
    user_id: int
    finish_at: bool
    items: list[ItemSchemaResquest]

#Responses
class ItemSchemaResponse(BaseModel):
    id: int
    product_id: int
    quantity: int 

    

class CartSchemaResponse(BaseModel):
    id: int
    user_id: int
    items: Union[list[ItemSchemaResponse], None]
    class Config:
            orm_mode = True


class CartSchemaResponse(BaseModel):
    carts: list[CartSchemaResponse]

class ItemSchemaResquestUpdate(BaseModel):
    product_id: int
    quantity: int
    
    @validator('quantity')
    def quantity_greatter_zero(cls, v):
        if v < 1:
            raise ValueError('Quantity must be greater than zero')
        return v

    class Config:
        orm_mode = True