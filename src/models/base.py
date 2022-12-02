from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from settings.db import DBConfig

SQLALCHEMY_DATABASE_URL = DBConfig().as_url(credentials=True)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(bind=engine)

AlchemyBaseModel = declarative_base(bind=engine)


def get_db():
    """
    Get SQLAlchemy database session
    """
    database = SessionLocal()
    try:
        yield database
    finally:
        database.close()


def add_autocommit(db: SessionLocal, instance):
    db.add(instance)
    db.commit()
    db.refresh(instance)
    return instance
