from pydantic import BaseModel, Field
from datetime import date


class FullTask(BaseModel):
    taskId: int
    taskName: str 
    taskDescription: str 
    taskType: str 
    taskComplete: bool
    plannedDate: date = Field(None, format="%Y-%m-%d")

    class Config:
        orm_mode = True
