from email.policy import default

from sqlalchemy import Boolean, Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

from app.database.database_helper import Base


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
   
    product_id = Column(Integer,nullable=False, index=True)
    quantity = Column(Integer,nullable=False)
    cart_id = Column(ForeignKey('carts.id'), index=True)
    cart = relationship("Cart", back_populates="items")

    def __repr__(self):
        return "<Item(id='%s', product_id='%s', quantity='%s', cart_id='%s')>" % (
                self.id, 
                self.product_id, 
                self.quantity, 
                self.cart_id,
                
            )
    
    
        

    


    
    
    
