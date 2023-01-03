from sqlalchemy import (
    Column,
    String,
    Integer,
    Enum,
    Boolean,
    DateTime,
    Date,
    ForeignKey,
)
import datetime

from databases.base import Base


class Task(Base):
    __tablename__ = "tasks"
    taskId = Column(Integer, primary_key=True)
    userId = Column(Integer, ForeignKey("users.userId"))
    taskName = Column(String(length=30), nullable=False)
    taskDescription = Column(String(length=200))
    taskType = Column(Enum("core", "project", "tool", name="task_type_enum"))
    taskComplete = Column(Boolean)
    createdTime = Column(DateTime, default=datetime.datetime.utcnow())
    plannedDate = Column(Date)
    completeTime = Column(DateTime, default=None)

    def __init__(self, userId: int, taskName: str, taskDescription: str, taskType: str, plannedDate: str):
        self.userId = userId
        self.taskName = taskName
        self.taskDescription = taskDescription
        self.taskType = taskType
        self.taskComplete = False
        self.plannedDate = datetime.datetime.strptime(plannedDate, "%Y-%m-%d").date()

    def __repr__(self):
        return f"<Task taskId={self.taskId} userId={self.userId} name={self.taskName} complete={self.taskComplete}>"

    def complete_task(self) -> None:
        current_time = datetime.datetime.utcnow() 
        self.taskComplete = True 
        self.completeTime = current_time
