import os
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
from app.constants import (
    HTTP_200_OK,
    DEFAULT_EXPIRED_TIME,
    EXPIRED_TIME_IN_MINUTES_KEY,
)


@router.post("/register", 
        status_code=HTTP_200_OK,
        response_model=ResponseUser)
def get_all_users(request_user: RequestUser, session: Session = Depends(get_session)):
    user_controller = UserController(session)

    if not user_controller.is_existed(username=request_user.username):
        user_controller.create_new_user(username=request_user.username, password=request_user.password)

    user = user_controller.get_user_by_name(request_user.username)
    return user

@router.post("/login",
        status_code=HTTP_200_OK,
        response_model=ResponseWithToken)
def login(request_user: RequestUser, session: Session = Depends(get_session)):
    user_controller = UserController(session)
    user = user_controller.get_response_user_by_name(request_user.username)
    expired_time_in_minutes = os.getenv(EXPIRED_TIME_IN_MINUTES_KEY, DEFAULT_EXPIRED_TIME)

    token = create_token(data={UserController.USER_ID_KEY: user.userId}, 
                            expired_delta=timedelta(minutes=expired_time_in_minutes))

    return ResponseWithToken(user=user, token=token)
