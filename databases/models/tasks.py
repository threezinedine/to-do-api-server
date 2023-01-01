from sqlalchemy import (
    Column,
    String,
    Integer,
    Enum,
    Boolean,
    DateTime,
    Date,
)
import datetime

from databases.base import Base


class Task(Base):
    __tablename__ = "tasks"
    taskId = Column(Integer, primary_key=True, index=True)
    taskName = Column(String(length=30), nullable=False)
    taskDescription = Column(String(length=200))
    taskType = Column(Enum("core", "project", "tool", name="task_type_enum"))
    taskComplete = Column(Boolean)
    createdTime = Column(DateTime, default=datetime.datetime.utcnow())
    plannedDate = Column(Date)
    completeTime = Column(DateTime, default=None)

    def __init__(self, taskName: str, taskDescription: str, taskType: str, plannedDate: datetime.datetime):
        self.taskName = taskName
        self.taskDescription = taskDescription
        self.taskType = taskType
        self.taskComplete = False
        self.plannedDate = plannedDate

    def __repr__(self):
        return f"<Task id={self.taskId} name={self.taskName} type={self.taskType} complete={self.taskComplete}>"

    def complete_task(self):
        current_time = datetime.datetime.utcnow() 
        self.taskComplete = True 
        self.completeTime = current_time
