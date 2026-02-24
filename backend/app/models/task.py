# uuid is used to generate unique identifiers for tasks
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime, Text, Enum
import enum
from app.core.database import Base

# Define an enumeration for task status
# This allows us to restrict the status of a task to specific values (pending, started, completed)
class TaskStatus(str, enum.Enum):
    PENDING = "pending"
    STARTED = "started"
    COMPLETED = "completed"


# Define the Task model which represents a task in the database
class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    status = Column(Enum(TaskStatus),nullable=False, default=TaskStatus.PENDING)
    org_id = Column(String, nullable=False, index=True)
    created_by = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

