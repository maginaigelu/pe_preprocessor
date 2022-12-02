from sqlalchemy import Column, Integer, Text, TIMESTAMP, BigInteger

from models.base import AlchemyBaseModel


class FilesMetadata(AlchemyBaseModel):
    __tablename__ = 'files_metadata'

    id = Column(Integer, primary_key=True, index=True)
    path = Column(Text, nullable=False)
    architecture = Column(Text, nullable=False)
    file_type = Column(Text, nullable=False)
    imports = Column(Integer, nullable=False)
    exports = Column(Integer, nullable=False)
    length = Column(Integer, nullable=False)
    hash = Column(BigInteger, index=True, unique=True, nullable=False)
