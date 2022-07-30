from app.database.database_helper import Base
from app.helpers.exceptions_helper import CupomException, GenericNotFoundException
from app.mock_services.cupom_service import get_cupom_params_by_name
from app.mock_services.product_service import get_product_params_by_id
from app.models.product_model import Product
from sqlalchemy import Column, DateTime, ForeignKey, Integer, select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    finish_at = Column(DateTime(timezone=True), default=None)
    user_id = Column(Integer, nullable=False)
    items = relationship("Item", back_populates="cart")

    cupoms_id = Column(ForeignKey("cupoms.id"), index=True)
    cupoms = relationship("Cupom", back_populates="cupoms")

    def __repr__(self):
        cupoms = self.cupoms if self.cupoms else None
        return (
            "<Cart(id='%s', user_id='%s', finish_at='%s' , items ='%s',  cupoms='%s')>"
            % (self.id, self.user_id, self.finish_at, self.items, cupoms)
        )

    @property
    def finished(self):
        if self.finish_at:
            return True
        return False

    async def validate_cupom_and_apply(self, cupom_name, db_session):

        db_cupom = None

        if cupom_name is not None and len(cupom_name) > 0:
            db_cupom = await get_cupom_params_by_name(cupom_name, db_session)
            if not db_cupom.active:
                raise CupomException(
                    "Cupom not valid",
                )
        self.cupoms_id = db_cupom.id if db_cupom else None
        return db_cupom

    async def validate_items(self, items, db_session):

        errors = list()
        for item in items:
            try:
                product = await get_product_params_by_id(item.product_id, db_session)
                product = product[0]

                if not product.in_stock:
                    errors.append(
                        {"id": product.id, "message": "Product not available"}
                    )

            except GenericNotFoundException:
                errors.append(
                    {"product id": item.product_id, "message": "Product not found"}
                )

        return errors
