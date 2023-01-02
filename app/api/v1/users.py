from fastapi import (
    Depends,
)
from sqlalchemy.orm import Session
from datetime import timedelta

from app.api.v1 import router
from databases.connection import (
    get_session,
)
from app.schemas import (
    RequestUser,
    ResponseUser,
    ResponseWithToken,
)
from app.controllers import UserController
from app.auth import create_token


@router.post("/register", 
        status_code=200,
        response_model=ResponseUser)
def get_all_users(request_user: RequestUser, session: Session = Depends(get_session)):
    user_controller = UserController(session)
    user_controller.create_new_user(username=request_user.username, password=request_user.password)

    user = user_controller.get_user_by_name(request_user.username)
    return user

@router.post("/login",
        status_code=200,
        response_model=ResponseWithToken)
def login(request_user: RequestUser, session: Session = Depends(get_session)):
    user_controller = UserController(session)
    user = user_controller.get_response_user_by_name(request_user.username)

    token = create_token(data={"userId": user.userId}, 
                            expired_delta=timedelta(minutes=15))

    return {
            "user": user,
            "token": token
        }
