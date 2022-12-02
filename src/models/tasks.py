from sqlalchemy import Column, Integer, Text

from models.base import AlchemyBaseModel


class Task(AlchemyBaseModel):

    __tablename__ = 'tasks'

    id = Column(Integer, primary_key=True, index=True)
    status = Column(Text,  nullable=False, default='In progress')

