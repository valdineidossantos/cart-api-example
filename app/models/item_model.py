from email.policy import default

from app.database.database_helper import Base
from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship




class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    cart_id = Column(Integer, ForeignKey('carts.id'))
    product_id = Column(Integer,nullable=False)
    quantity = Column(Integer,nullable=False)
    cart = relationship("Cart")
    
        

    

