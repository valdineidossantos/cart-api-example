from app.database.database_helper import db_session
from app.helpers.exceptions_helper import GenericNotFoundException
from app.models.product_model import Product
from app.repository.product_repository import ProductRepository
from app.schemas.product_schemas import ProductCreate, ProductUpdate
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

router = APIRouter(prefix="/v1/products", tags=["products"])


@router.get("/", status_code=status.HTTP_200_OK)
async def get_all_products(db_session: AsyncSession = Depends(db_session)):
    product_repository = ProductRepository(db_session, Product)
    return await product_repository.get_all()


@router.get("/{product_id}", status_code=status.HTTP_200_OK)
async def get_products_by_id(
    product_id: int, db_session: AsyncSession = Depends(db_session)
):
    product_repository = ProductRepository(db_session, Product)
    try:
        return await product_repository.get_by_id(product_id)
    except GenericNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_product(
    new_product: ProductCreate, db_session: AsyncSession = Depends(db_session)
):
    product_repository = ProductRepository(db_session, Product)
    product = Product(
        name=new_product.name,
        short_name=new_product.short_name,
        description=new_product.description,
        category=new_product.category,
        price=new_product.price,
        quantity_stock=new_product.quantity_stock,
    )
    return await product_repository.create(product)


@router.delete("/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_product(
    product_id: int, db_session: AsyncSession = Depends(db_session)
):
    product_repository = ProductRepository(db_session, Product)
    await product_repository.delete(product_id)
    return ""


@router.put("/{product_id}", status_code=status.HTTP_200_OK)
async def update_product(
    update_product: ProductUpdate,
    product_id: int,
    db_session: AsyncSession = Depends(db_session),
):
    product_repository = ProductRepository(db_session, Product)
    product = Product(
        name=update_product.name,
        short_name=update_product.short_name,
        description=update_product.description,
        category=update_product.category,
        price=update_product.price,
        quantity_stock=update_product.quantity_stock,
        id=product_id,
        in_stock=update_product.in_stock,
    )
    try:
        return await product_repository.update(product)
    except GenericNotFoundException:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Product not found"
        )
