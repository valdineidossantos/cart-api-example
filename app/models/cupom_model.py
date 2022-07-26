from sqlalchemy import Boolean, Column, Float, Integer, String
from sqlalchemy.orm import relationship

from app.database.database_helper import Base


class Cupom(Base):
    __tablename__ = "cupoms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=50), nullable=False, index=True, unique=True)
    discount = Column(Float, nullable=False)
    active = Column(Boolean, default=True)

    cupoms = relationship("Cart", back_populates="cupoms")

    def __repr__(self):
        return "<Cupom(id='%s', name='%s', discount='%s', active='%s')>" % (
            self.id,
            self.name,
            self.discount,
            self.active
        )
    
        


