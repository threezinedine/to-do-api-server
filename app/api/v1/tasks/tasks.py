from fastapi import (
    Depends,
)
from typing import List
from sqlalchemy.orm import Session

from databases.connection import get_session
from app.controllers import (
    UserController,
    TaskController,
)
from app.schemas import FullTask
from databases.models import Task
from app.api.v1.tasks import router
from app.auth import get_current_user_from_token


@router.get("/",
        response_model=List[FullTask])
def get_all_tasks(user_info: int = Depends(get_current_user_from_token), session: Session = Depends(get_session)):
    user_controller = UserController(session)
    task_controller = TaskController(session, user_controller)

    user = user_controller.get_user_by_id(userId=user_info["userId"])
    tasks = task_controller.get_all_tasks_by_username(username=user.username)

    return tasks
