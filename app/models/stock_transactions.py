from sqlalchemy import Boolean, Column, Integer, String, DateTime, Float, ForeignKey
from sqlalchemy.orm import relationship

from database.db import Base

class AccountStockTransactions(Base):
    __tablename__ = "account_stoc_transaction"
    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float)
    creation_date = Column(DateTime)
    status = Column(String)
    price = Column(Float)
    ticker = Column(String)
    cash_transaction = relationship("AccountCashTransaction", overlaps="account_stoc_transaction")