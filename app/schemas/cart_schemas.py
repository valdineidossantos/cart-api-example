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
