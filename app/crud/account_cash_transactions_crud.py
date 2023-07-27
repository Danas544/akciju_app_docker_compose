from sqlalchemy.orm import Session
from sqlalchemy.orm.exc import NoResultFound
from typing import Optional, List

from models.account_cash_transactions import AccountCashTransaction
import schemas.account_cash_transaction_schemas
from crud.account_crud import get_account
from sqlalchemy import and_, join
from models.stock_transactions import AccountStockTransactions

def create_transaction(
    db: Session,
    account_id,
    account_cash_transaction: schemas.account_cash_transaction_schemas.AccountCashTransactionCreate,
    account_stoc_transaction = None) -> Optional[AccountCashTransaction]:
    db_account = get_account(db, account_id)
    if db_account:
        if account_stoc_transaction is None:
            db_account_cash_transaction = AccountCashTransaction(
            amount=account_cash_transaction.amount,
            creation_date=account_cash_transaction.creation_date,
            status=account_cash_transaction.status
        )
        else:
            db_account_cash_transaction = AccountCashTransaction(
            amount=account_cash_transaction.get('amount'),
            creation_date=account_cash_transaction.get("creation_date"),
            status=account_cash_transaction.get("status"),
            account_stoc_transaction=account_stoc_transaction
            )

        db_account.transactions.append(db_account_cash_transaction)
        db.add(db_account_cash_transaction)
        db.commit()
        db.refresh(db_account_cash_transaction)
        return db_account_cash_transaction
    else:
        raise NoResultFound


def get_transactions(db: Session, account_id: int) -> List[AccountCashTransaction]:
    return (
        db.query(AccountCashTransaction)
        .filter(AccountCashTransaction.account_id == account_id)
        .all()
    )


def get_balance(db: Session, account_id: int):
    all_account_transactions = get_transactions(db, account_id)
    return all_account_transactions


def get_stock_balance(db: Session, account_id: int , ticker_name:str):
    join_condition = AccountCashTransaction.account_stoc_transaction_id == AccountStockTransactions.id
    result = db.query(AccountCashTransaction).join(AccountStockTransactions, join_condition) \
                .filter(AccountCashTransaction.account_id == account_id,
                        AccountStockTransactions.ticker == ticker_name) \
                .all()
    
    return result






