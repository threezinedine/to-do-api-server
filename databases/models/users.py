from sqlalchemy import (
    Column,
    Integer,
    String,
)

from databases.base import Base
from app.auth import get_hased_password, verify_the_password


class User(Base):
    __tablename__ = "users"
    userId = Column(Integer, primary_key=True, index=True)
    username = Column(String(length=30), unique=True)
    password = Column(String(length=50))
    description = Column(String(length=200))
    imagePath = Column(String(length=50), default=None)

    def __init__(self, username: str, password: str, description: str):
        self.username = username
        self.password = get_hased_password(password)
        self.description = description

    def __repr__(self):
        return f"<User id={self.userId} username={self.username}>"

    def compared_password(self, password: str) -> bool:
        return verify_the_password(self.password, password)
