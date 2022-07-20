from typing import Union
from pydantic import BaseModel


class ProductCreate(BaseModel):
    name: str
    short_name: str
    description: Union[str, None] = None
    active: Union[bool, None] = True
    category: Union[str, None] = None
    price: float
    in_stock: Union[bool, None] = True

    class Config:
        orm_mode = True

class ProductUpdate(BaseModel):
    name: str
    short_name: str
    description: Union[str, None] = None
    active: Union[bool, None] = True
    category: Union[str, None] = None
    price: float
    in_stock: Union[bool, None] = True

    class Config:
        orm_mode = True
