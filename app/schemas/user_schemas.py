import re
from enum import Enum
from typing import Union

from pydantic import BaseModel, validator

regex = "^[a-z0-9]+[\\._]?[a-z0-9]+[@]\\w+[.]\\w{2,3}$"


def valid_email(email):

    if re.search(regex, email):
        return True
    return False


class UserCreate(BaseModel):
    name: str
    email: str
    active: Union[bool, None] = True

    @validator("email")
    def validate_email(cls, v):
        if not valid_email(v):
            raise ValueError("Type a valid email")
        return v

    class Config:
        orm_mode = True


class UserUpdate(UserCreate):
    class Config:
        orm_mode = True
