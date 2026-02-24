from datetime import datetime
from pydantic import BaseModel
from typing import Optional
from app.models.task import TaskStatus

# Define a Pydantic model for creating a new task
class TaskCreate(BaseModel):
    title: str
    description: Optional[str] = None
    status: TaskStatus = TaskStatus.PENDING


# Define a Pydantic model for updating an existing task
class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[TaskStatus] = None

# Define a Pydantic model for updating the status of a task
class TaskStatusUpdate(BaseModel):
    status: TaskStatus

# Define a Pydantic model for representing a task in responses
class TaskResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    status: TaskStatus
    created_by: str
    created_at: datetime
    updated_at: datetime

# This configuration allows Pydantic to create a TaskResponse model from a SQLAlchemy Task model
    class Config:
        from_attributes = True

