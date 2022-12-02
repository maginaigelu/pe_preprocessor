from pydantic import Field

from api.core.schemas import BaseModel


class FilesMetadata(BaseModel):

    id: int = Field()
    path: str = Field()
    architecture: str = Field()
    file_type: str = Field()
    imports: int = Field()
    exports: int = Field()
    length: str = Field()
    hash: int = Field()

    class Config:
        orm_mode = True
