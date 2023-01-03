from fastapi import (
    Depends,
)
from sqlalchemy.orm import Session

from databases.connection import get_session
from app.controllers import (
    UserController,
    TaskController,
)
from app.api.v1.tasks import router
from app.auth import get_current_user_from_token


@router.get("/")
def get_all_tasks(userId: int = Depends(get_current_user_from_token), session: Session = Depends(get_session)):
    user_controller = UserController(session)
    task_controller = TaskController(session, user_controller)

    user = user_controller.get_user_by_id(userId=userId)

    return []
