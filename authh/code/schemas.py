from dataclasses import dataclass
from datetime import datetime

from pydantic import BaseModel


class CreateUserSchema(BaseModel):
   name: str
   surname: str
   email: str
   username: str
   password: str


class UserAllOptionalSchema(BaseModel):
   username: None | str
   password: None | str


@dataclass
class LoginRequestModel:
   username: str
   password: str


@dataclass
class TokenData:
   role: str
   sub: int
   exp: datetime | None = None



