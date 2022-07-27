import datetime
from enum import Enum
from typing import Union

from pydantic import BaseModel, validator


class CupomRequest(BaseModel):
    name: str
    discount: float
    active: bool = True

    @validator("discount")
    def quantity_greatter_zero(cls, v):
        if v < 1:
            raise ValueError("Discount value must be greater than zero")
        return v

    class Config:
        orm_mode = True
