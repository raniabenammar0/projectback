from typing import Optional
from pydantic import BaseModel
import datetime


class CognitoModel(BaseModel):
    sub: Optional[str]
    email: Optional[str]


class UserModel(BaseModel):
    userName: str
    email: str
    credit: Optional[int]   = None
    lastName: Optional[str] = None
    phone: Optional[int] = None
    cognito: Optional[CognitoModel]
    firstLogin: bool = True
    createdAt: Optional[datetime.datetime] = datetime.datetime.now()
    updatedAt: Optional[datetime.datetime] = datetime.datetime.now()
    deletedAt: Optional[datetime.datetime] = None

