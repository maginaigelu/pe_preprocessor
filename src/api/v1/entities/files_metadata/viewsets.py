from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.sqlalchemy import paginate
from sqlmodel import Session

from api.v1.entities.files_metadata.schemas import FilesMetadata
from models import FilesMetadata as ModelFilesMetadata
from models.base import get_db

router = APIRouter()


@router.get("/files_metadata/", response_model=Page[FilesMetadata])
async def get_files_metadata(db: Session = Depends(get_db), params: Params = Depends()):
    return paginate(db.query(ModelFilesMetadata), params)


@router.get("/files_metadata/{metadata_id}", response_model=FilesMetadata)
async def get_file_metadata(metadata_id, db: Session = Depends(get_db)):
    return db.query(ModelFilesMetadata).get()
