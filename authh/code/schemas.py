from pydantic import BaseModel


class CreateUserSchema(BaseModel):
   name: str
   surname: str
   email: str
   username: str
   password: str


class UserInDB(CreateUserSchema):
   id: int
   date_registered: str

