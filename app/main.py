from fastapi import FastAPI

from app.database.database_helper import db_session
from app.routes.cart import router as cart_router
from app.routes.cupom import router as cupom_router
from app.routes.product import router as product_router
from app.routes.user import router as user_router


def get_db():
    return db_session


def get_app():
    app = FastAPI()
    app.include_router(product_router)
    app.include_router(user_router)
    app.include_router(cart_router)
    app.include_router(cupom_router)
    return app


app = get_app()


@app.get("/")
async def read_root():
    return "Start Page"
