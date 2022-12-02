from fastapi import APIRouter, Depends
from sqlmodel import Session

from api.v1.entities.s3.schemas import S3TasksByCount
from api.v1.entities.tasks.schemas import TasksStatus
from dramatiq_tasks.tasks import process_pe_from_s3

from models import Task
from models.base import get_db, add_autocommit

router = APIRouter()


@router.post("/from_s3/", response_model=TasksStatus)
async def get_n_task(request: S3TasksByCount, db: Session = Depends(get_db)):
    task = add_autocommit(db, Task())
    process_pe_from_s3.send(
        bucket=request.bucket,
        cnt=request.n,
        page_size=request.page_size,
        task_id=task.id)
    return task
