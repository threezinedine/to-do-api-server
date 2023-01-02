from pydantic import BaseModel

from databases.models import User


class RequestUser(BaseModel):
    username: str 
    password: str

    class Config:
        orm_mode = True


class ResponseUser(BaseModel):
    userId: int
    username: str

    class Config:
        orm_mode = True


class FullUserWithoutPassword(ResponseUser):
    description: str 
    image: str


class FullUser(FullUserWithoutPassword):
    password: str


class ResponseWithToken(BaseModel):
    user: FullUserWithoutPassword
    token: str

    class Config:
        orm_mode = True
