import datetime
from enum import Enum
from typing import Union
from pydantic import BaseModel, validator


class Items(BaseModel):
    product_id: int
    product_quantity: int


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
    def __init__(self, product_id: int, product_quantity: int, cart_id: int):
        self.product_id = product_id
        self.product_quantity = product_quantity
        self.cart_id = cart_id
    product_id: int
    quantity: int    

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



class CartSchemaResponse(BaseModel):
    carts: list[CartSchemaResponse]

