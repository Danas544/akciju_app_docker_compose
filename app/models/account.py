from sqlalchemy import Boolean, Column, Integer, String, DateTime
from sqlalchemy.orm import relationship

from database.db import Base


class Account(Base):
    __tablename__ = "accounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    email = Column(String, unique=True, index=True)
    password = Column(String)
    birthdate = Column(DateTime)
    phone_number = Column(String)
    is_active = Column(Boolean, default=True)

    transactions = relationship("AccountCashTransaction", back_populates="account")
