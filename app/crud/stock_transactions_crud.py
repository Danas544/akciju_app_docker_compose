from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional, List

from models.stock_transactions import AccountStockTransactions
import schemas.account_cash_transaction_schemas
from crud.account_crud import get_account
from sqlalchemy import and_
from datetime import datetime

def create_stock_transaction(db: Session,account_id: int,ticker: dict,amount: float, status:str):
    db_account = get_account(db, account_id)
    if db_account:
        db_account_stock_transaction = AccountStockTransactions(
            amount=amount,
            creation_date=datetime.now(),
            status=status,
            price=ticker.get('price'),
            ticker=ticker.get('name')
        )


        return db_account_stock_transaction
    else:
        raise NoResultFound
    

