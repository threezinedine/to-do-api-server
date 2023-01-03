from sqlalchemy.orm import Session
from typing import List

from databases.models import Task
from app.controllers import UserController


class TaskController:
    def __init__(self, session: Session, user_controller: UserController):
        self.session = Session
        self.user_controller = user_controller

    def get_all_tasks_by_username(self, username: str) -> List[Task]:
        user = self.user_controller.get_user_by_name(username)
        return user.tasks
