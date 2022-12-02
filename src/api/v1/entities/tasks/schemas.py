from api.core.schemas import BaseModel


class TasksStatus(BaseModel):

    id: int
    status: str

    class Config:
        orm_mode = True
