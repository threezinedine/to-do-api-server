from pydantic import BaseModel


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
