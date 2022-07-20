from typing import Union
from urllib.error import HTTPError

from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.exc import NoResultFound


from app.database.database_helper import db_session
from app.helpers.exceptions_helper import ProductNotFound
from app.models.product_model import Product
from app.repository.product_repository import ProductRepository
from app.schemas.product_schemas import ProductCreate, ProductUpdate

from app.routes.product import router as product_router
from app.routes.user import router as user_router


app = FastAPI()

@app.get("/")
async def read_root():
    return "Start Page"

app.include_router(product_router)
app.include_router(user_router)
