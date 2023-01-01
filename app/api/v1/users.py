from fastapi import (
    Depends,
)
from sqlalchemy.orm import Session

from app.api.v1 import router
from databases.connection import (
    get_session,
)
from app.schemas import (
    RequestUser,
    ResponseUser,
)
from app.controllers import UserController


@router.post("/register", 
        status_code=200,
        response_model=ResponseUser)
def get_all_users(request_user: RequestUser, session: Session = Depends(get_session)):
    user_controller = UserController(session)
    user_controller.create_new_user(username=request_user.username, password=request_user.password)

    user = user_controller.get_by_name(request_user.username)
    return user

