from pydantic import BaseModel
from sqlalchemy import Column, Integer, Float
from sqlalchemy.orm import declarative_base

Base = declarative_base()

# Pydantic model for account creation (used for request validation)
class AccountCreate(BaseModel):
    balance: float

    class Config:
        orm_mode = True  # Ensures Pydantic models work with ORM models (SQLAlchemy)

# SQLAlchemy model for account
class Account(Base):
    __tablename__ = 'accounts'

    id = Column(Integer, primary_key=True, index=True)
    balance = Column(Float, nullable=False)
