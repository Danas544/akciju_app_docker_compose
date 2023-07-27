from datetime import datetime
from typing import Optional, Literal

from pydantic import BaseModel, EmailStr


class Ticker_price(BaseModel):
    name: str
    price: float
    date: datetime


    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Antantas",
                "price": 1619.06,
                "date": "2023-07-11T18:08:57.215Z",
            }
        }


class Buy_sell_ticker(BaseModel):
    amount: float
    type: Literal['BUY','SELL']
    date: datetime
        


    class Config:
            orm_mode = True
            schema_extra = {
                "example": {
                    "amount": 161,
                    "type": "BUY,SELL",
                    "date": "2023-07-11T18:08:57.215Z"
                }
            }
    

class Ticker_amount(BaseModel):
     ticker: str
     amount: float
     date: datetime

     class Config:
            orm_mode = True
            schema_extra = {
                "example": {
                    "ticker": "AMZ",
                    "amount": 2,
                    "date": "2023-07-11T18:08:57.215Z"
                }
            }