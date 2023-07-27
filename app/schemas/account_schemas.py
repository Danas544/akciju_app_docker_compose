from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr


class AccountCreate(BaseModel):
    name: str
    surname: str
    email: EmailStr
    password: str
    birthdate: datetime
    phone_number: Optional[str]

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "Antantas",
                "surname": "Fontanas",
                "email": "antantas123@gmail.com",
                "password": "1234",
                "birthdate": "2023-07-11T18:08:57.215Z",
                "phone_number": "123456",
            }
        }


class AccountResponse(BaseModel):
    id: int
    name: str
    surname: str
    email: EmailStr
    password: str
    birthdate: datetime
    phone_number: Optional[str]

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "id": 1,
                "name": "Antantas",
                "surname": "Fontanas",
                "email": "antantas123@gmail.com",
                "password": "1234",
                "birthdate": "2023-07-11T18:08:57.215Z",
                "phone_number": "123456",
            }
        }


class AccountUpdate(BaseModel):
    name: Optional[str]
    surname: Optional[str]
    email: Optional[EmailStr]
    password: Optional[str]
    birthdate: Optional[datetime]
    phone_number: Optional[str]

    class Config:
        orm_mode = True
        json_schema_extra = {
            "example": {
                "name": "Antantas",
                "surname": "Fontanas",
                "email": "antantas123@gmail.com",
                "password": "1234",
                "birthdate": "2023-07-11T18:08:57.215Z",
                "phone_number": "123456",
            }
        }
