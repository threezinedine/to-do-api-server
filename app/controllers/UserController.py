from typing import (
    Union,
)
from sqlalchemy.orm import Session
from databases.models import User
from app.schemas import (
    FullUser,
)


class UserController:
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_name(self, username: str) -> Union[User, None]:
        return self.session.query(User).filter(User.username==username).first()

    def get_response_user_by_name(self, username: str) -> Union[FullUser, None]:
        response_user = None
        user = self.get_user_by_name(username)

        if user is not None:
            response_user = FullUser(userId=user.userId, 
                                        username=user.username, 
                                        password=user.password,
                                        description=user.description,
                                        image=""
                                    )
        return response_user

    def create_new_user(self, username: str, password: str) -> None:
        user = User(username=username, password=password, description="")

        self.session.add(user)
        self.session.commit()
