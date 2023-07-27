from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from sqlalchemy.orm.exc import NoResultFound
from database.db import get_db
import crud.account_cash_transactions_crud, crud.account_crud, crud.stock_transactions_crud

from schemas.account_cash_transaction_schemas import (
    AccountCashTransactionCreate,
    AccountCashTransactionResponse,
    AccountCashBalanceResponse,
)
from schemas.tickers import Ticker_price, Buy_sell_ticker, Ticker_amount
from datetime import datetime
from endpoints.account_cash_transactions_api import get_account_balance
import finnhub


router = APIRouter()
finnhub_client = finnhub.Client(api_key="civvqfhr01qlkaevujp0civvqfhr01qlkaevujpg")


def get_stock_price(name: str) -> Optional[float]:
    try:
        res = finnhub_client.quote(name)
        price = res.get("c")
        if price == 0:
            return None
        return price
    except:
        return price


@router.get("/{ticker}", response_model=Ticker_price)
def get_ticker(ticker: str):
    price = get_stock_price(ticker)
    if price is not None:
        json_body = {"name": ticker, "price": price, "date": datetime.now()}
        return json_body
    else:
        raise HTTPException(status_code=404, detail=f"Stock {ticker} not found")


@router.post("/{account_id}/{ticker}")
def buy_sell_ticker(
    ticker: str,
    account_id: int,
    Buy_sell_ticker: Buy_sell_ticker,
    db: Session = Depends(get_db),
):
    ticker_body = get_ticker(ticker)

    db_account = crud.account_crud.get_account(db, account_id)
    if db_account:
        ticker_sum = Buy_sell_ticker.amount * ticker_body.get("price")
        if Buy_sell_ticker.type == "BUY":
            account_balance = get_account_balance(account_id=account_id, db=db)
            if account_balance.get("amount") > ticker_sum:
                try:
                    create_stock_tran = (
                        crud.stock_transactions_crud.create_stock_transaction(
                            account_id=account_id,
                            db=db,
                            ticker=ticker_body,
                            amount=Buy_sell_ticker.amount,
                            status="BUY",
                        )
                    )
                except NoResultFound:
                    raise HTTPException(
                        status_code=404, detail=f"Account {account_id} not found"
                    )
                account_cash_transaction = {
                    "amount": ticker_sum,
                    "creation_date": create_stock_tran.creation_date,
                    "status": "BUYING-SHARES",
                }
                try:
                    create_cash_tran = (
                        crud.account_cash_transactions_crud.create_transaction(
                            db=db,
                            account_id=account_id,
                            account_cash_transaction=account_cash_transaction,
                            account_stoc_transaction=create_stock_tran,
                        )
                    )
                except NoResultFound:
                    raise HTTPException(
                        status_code=404, detail=f"Account {account_id} not found"
                    )
                return create_cash_tran
            else:
                raise HTTPException(
                    status_code=406,
                    detail=f"Low ballance {account_balance.get('amount')} please first TOP-UP",
                )
        else:
            account_ticker_amount = get_stock_amount(
                account_id=account_id, ticker=ticker_body.get("name"), db=db
            )
            if account_ticker_amount.get("amount") > Buy_sell_ticker.amount:
                try:
                    create_stock_tran = (
                        crud.stock_transactions_crud.create_stock_transaction(
                            account_id=account_id,
                            db=db,
                            ticker=ticker_body,
                            amount=Buy_sell_ticker.amount,
                            status="SELL",
                        )
                    )
                except NoResultFound:
                    raise HTTPException(
                        status_code=404, detail=f"Account {account_id} not found"
                    )

                account_cash_transaction = {
                    "amount": ticker_sum,
                    "creation_date": create_stock_tran.creation_date,
                    "status": "SELLING-SHARES",
                }
                try:
                    create_cash_tran = (
                        crud.account_cash_transactions_crud.create_transaction(
                            db=db,
                            account_id=account_id,
                            account_cash_transaction=account_cash_transaction,
                            account_stoc_transaction=create_stock_tran,
                        )
                    )
                except NoResultFound:
                    raise HTTPException(
                        status_code=404, detail=f"Account {account_id} not found"
                    )
                return create_cash_tran
            else:
                raise HTTPException(
                    status_code=406,
                    detail=f"Please first buy more {ticker_body.get('name')}",
                )

    else:
        raise HTTPException(status_code=404, detail=f"Account {account_id} not found")


@router.get("/{account_id}/{ticker}", response_model=Ticker_amount)
def get_stock_amount(account_id, ticker, db: Session = Depends(get_db)):
    db_account = crud.account_crud.get_account(db, account_id)
    if db_account:
        tickers = crud.account_cash_transactions_crud.get_stock_balance(
            db, account_id, ticker_name=ticker
        )
        amount = 0
        for ticker_db in tickers:
            if ticker_db.account_stoc_transaction.status == "BUY":
                amount += ticker_db.account_stoc_transaction.amount
            else:
                amount -= ticker_db.account_stoc_transaction.amount


        stock_amount = {"ticker": ticker, "amount": amount, "date": datetime.now()}
        return stock_amount

    else:
        raise HTTPException(status_code=404, detail=f"Account {account_id} not found")
