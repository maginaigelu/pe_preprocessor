from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlalchemy.orm import Session

from api.v1.entities.tasks.schemas import TasksStatus
from models import Task
from models.base import get_db

router = APIRouter()


@router.get("/tasks", response_model=Page[TasksStatus])
async def get_tasks(db: Session = Depends(get_db), params: Params = Depends()):
    return paginate(db.query(Task), params)


@router.get("/tasks/{task_id}", response_model=TasksStatus)
async def get_task(task_id, db: Session = Depends(get_db)):
    return db.query(Task).get(task_id)
