from sqlalchemy.ext.asyncio import AsyncSession

from app.helpers.exceptions_helper import GenericNotFoundException
from app.models.product_model import Product
from app.repository.product_repository import ProductRepository


async def get_product_params_by_id(
    product_id: int, db_session: AsyncSession
) -> Product:
    product_repository = ProductRepository(db_session, Product)

    product = await product_repository.get_by_id(product_id)

    if product:
        return product[0]

    raise GenericNotFoundException(message="Product not found")
