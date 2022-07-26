from sqlalchemy import Boolean, Column, Float, Integer, String
from sqlalchemy.orm import relationship

from app.database.database_helper import Base


class Cupom(Base):
    __tablename__ = "cupoms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=50), nullable=False, index=True)
    discount = Column(Float, nullable=False)
    
    cart =  relationship("Cart", back_populates="cart")
    active = Column(Boolean, default=True)

    cupoms = relationship("Cart", back_populates="cupoms")
    
        


