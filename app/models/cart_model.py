from email.policy import default
from app.database.database_helper import Base
from sqlalchemy import Boolean, Column, Integer, DateTime
from sqlalchemy.sql import func


class Cart(Base):
    __tablename__ = "carts"

    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    finish_at = Column(DateTime(timezone=True), default=None)
    user_id = Column(Integer, nullable=False)

    @property
    def finished(self):
        if self.finish_at: 
            return  True
        return False
    
    
        


