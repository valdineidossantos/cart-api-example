from sqlalchemy import Boolean, Column, Integer, String

from app.database.database_helper import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(length=200), nullable=False)
    email = Column(String(length=100), nullable=False, index=True)
    active = Column(Boolean, default=True)
    
        


