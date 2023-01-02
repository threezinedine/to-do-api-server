from typing import (
    Union,
)
from sqlalchemy.orm import Session
from databases.models import User
from app.schemas import (
    FullUser,
)


class UserController:
    USER_ID_KEY = "userId"
    USERNAME_KEY = "username"
    DESCRIPTION_KEY = "description"
    IMAGE_KEY = "image"
    PASSWORD_KEY = "password"
    USER_KEY = "user"
    TOKEN_KEY = "token"

    """
    The controller class for the users table.

    Paratemers
    ----------
        session: Session
            The database connection session.
    """
    def __init__(self, session: Session):
        self.session = session

    def get_user_by_name(self, username: str) -> Union[User, None]:
        """
        The method that get the user (ORM model) from the database

        Paratemers
        ----------
            username: str 
                The input username that will be searched in the database. 

        Returns
        -------
            user: User | None 
                Return the user if the username exists, otherwise, return None
        """
        return self.session.query(User).filter(User.username==username).first()

    def get_response_user_by_name(self, username: str) -> Union[FullUser, None]:
        """
        The method that gets the user by username then converts it into pydantic model.

        Paratemers
        ----------
            username: str 
                The input username that will be searched in the database. 

        Returns
        -------
            user: FullUser | None 
                Return the user if the username exists, otherwise, return None
        """
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
        """
        The method that create a user into the database.

        Paratemers
        ----------
            username: str 
                The input username.

            password: str 
                The raw password, which is encrypted before saving into the database.

        Returns
        -------
        """
        user = User(username=username, password=password, description="")

        self.session.add(user)
        self.session.commit()

    def is_existed(self, username: str) -> bool:
        """
        The medthod that checks whether username is created

        Paratemers
        ----------
            username: str 
                The checked username.

        Returns
        -------
            is_existed: bool 
                Return True if the username existed, vice versa
        """
        user = self.get_user_by_name(username)
        return user is not None
