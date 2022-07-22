from email.policy import default
from app.database.database_helper import Base
from sqlalchemy import Boolean, Column, Integer, DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship

from app.models.item_model import Item


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    finish_at = Column(DateTime(timezone=True), default=None)
    user_id = Column(Integer, nullable=False)
    
    items =  relationship("Item", back_populates="cart")
    

    def __repr__(self):
        return "<Cart(id='%s', user_id='%s', finish_at='%s' , items ='%s' )>" % (
                self.id, 
                self.user_id, 
                self.finish_at, 
                self.items
            )

    @property
    def finished(self):
        if self.finish_at: 
            return  True
        return False
    
    
        
