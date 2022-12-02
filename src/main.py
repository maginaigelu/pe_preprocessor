from fastapi import FastAPI

from api.v1.entities.files_metadata.viewsets import router as metadat_router
from api.v1.entities.s3.viewsets import router as s3_router
from api.v1.entities.tasks.viewsets import router as tasks_router

app = FastAPI()

app.include_router(s3_router)
app.include_router(tasks_router)
app.include_router(metadat_router)
