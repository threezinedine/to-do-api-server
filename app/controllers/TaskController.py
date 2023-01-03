from sqlalchemy.orm import Session
from typing import List
from datetime import datetime

from databases.models import Task
from app.controllers import UserController


class TaskController:
    def __init__(self, session: Session, user_controller: UserController):
        self.session = session
        self.user_controller = user_controller

    def get_all_tasks_by_username(self, username: str) -> List[Task]:
        user = self.user_controller.get_user_by_name(username)
        return user.tasks

    def create_new_task_by_username(self, username: str, 
                taskName: str, 
                taskDescription: str,
                taskType: str, 
                plannedDate: datetime) -> None:
        user = self.user_controller.get_user_by_name(username)

        task = Task(userId=user.userId, 
                        taskName=taskName, 
                        taskDescription=taskDescription, 
                        taskType=taskType, 
                        plannedDate=plannedDate)
        
        self.session.add(task)
        self.session.commit()
