

from app.database.database_helper import Base
from sqlalchemy import Column, DateTime, ForeignKey, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    finish_at = Column(DateTime(timezone=True), default=None)
    user_id = Column(Integer, nullable=False)
    items =  relationship("Item", back_populates="cart")
    
    cupoms_id = Column(ForeignKey('cupoms.id'), index=True)
    cupoms = relationship("Cupom", back_populates="cupoms")
    
    
    

    def __repr__(self):
        cupoms= self.cupoms if self.cupoms else None
        return "<Cart(id='%s', user_id='%s', finish_at='%s' , items ='%s',  cupoms='%s')>" % (
                self.id, 
                self.user_id, 
                self.finish_at, 
                self.items,                
                cupoms
                
            )

    @property
    def finished(self):
        if self.finish_at: 
            return  True
        return False
    
    
        
