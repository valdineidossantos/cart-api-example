from enum import Enum
from typing import Union

from pydantic import BaseModel, validator


#This categories need return from database
class Categories_Mock(str, Enum):
    Eletronics = "Eletronics"
    Books = "Books"
    Food = "Food"
    Clothes = "Clothes"
    Sports = "Sports"
    Others = "Others"

   


class ProductCreate(BaseModel):
    name: str
    short_name: str
    description: Union[str, None] = None
    active: Union[bool, None] = True
    category: Union[Categories_Mock, None] = None
    price: float
    in_stock: Union[bool, None] = True
    quantity_stock: int = 0

    @validator('quantity_stock')
    def quantity_stock_greatter_zero(cls, v):
        if v < 0:
            raise ValueError('Quantity stock must be greater than zero')
        return v

    class Config:
        orm_mode = True

class ProductUpdate(ProductCreate):

    class Config:
        orm_mode = True
