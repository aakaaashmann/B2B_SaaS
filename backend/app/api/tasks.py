from fastapi import APIRouter, Depends, HTTPException, status
from datetime import datetime
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.auth import get_current_user, require_view, require_create, require_delete, require_edit, AuthUser
from typing import List
from app.models.task import Task
from app.schemas.task import TaskCreate, TaskUpdate, TaskStatusUpdate, TaskResponse

# This file defines the API endpoints for managing tasks, including creating, reading, updating, and deleting tasks.
router = APIRouter(prefix="/api/task", tags =["tasks"])

# The following endpoints allow users to perform CRUD operations on tasks, with appropriate permissions checks and error handling.
@router.get(path="",response_model=List[TaskResponse])
def list_tasks(user: AuthUser = Depends(require_view), db: Session = Depends(get_db)):
    tasks = db.query(Task).filter(Task.org_id == user.org_id).all()
    return tasks

@router.post(path="", response_model=TaskResponse, status_code=status.HTTP_201_CREATED)
def create_task(task_data: TaskCreate, 
                user: AuthUser = Depends(require_create), # Ensure the user has permission to create a task
                db: Session = Depends(get_db)
    ):
    tasks = Task(
        title=task_data.title,
        description=task_data.description,
        status=task_data.status,
        org_id=user.org_id,
        created_by=user.user_id
    )
    db.add(tasks)
    db.commit()
    db.refresh(tasks)
    return tasks

@router.get(path="/{task_id}", response_model=TaskResponse)
def get_task(task_id: str,
             user: AuthUser = Depends(require_view), # Ensure the user has permission to view the task
             db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.org_id == user.org_id
    ).first()

    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    return task

@router.put(path="/{task_id}", response_model=TaskResponse)
def update_task(task_id: str,
                task_data: TaskUpdate,
                user: AuthUser = Depends(require_edit), # Ensure the user has permission to edit the task
                db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.org_id == user.org_id
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    if task_data.title is not None:
        task.title = task_data.title # Update the title of the task if provided in the request
    if task_data.description is not None:
        task.description = task_data.description # Update the description of the task if provided in the request
    if task_data.status is not None:
        task.status = task_data.status # Update the status of the task if provided in the request
    task.updated_at = datetime.utcnow() # Update the timestamp of when the task was last updated
    db.commit()
    db.refresh(task)
    return task

@router.delete(path="/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: str,
                user: AuthUser = Depends(require_delete), # Ensure the user has permission to delete the task
                db: Session = Depends(get_db)
):
    task = db.query(Task).filter(
        Task.id == task_id,
        Task.org_id == user.org_id
    ).first()
    if not task:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )
    db.delete(task)
    db.commit()
    return None 