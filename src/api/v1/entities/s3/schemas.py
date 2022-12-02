from pydantic import Field

from api.core.schemas import BaseModel


class S3TasksByCount(BaseModel):

    n: int
    bucket: str
    page_size: int = Field(1000)
