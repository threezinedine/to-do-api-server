import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from databases.base import Base


database_name = os.getenv("DATABASE_URL", "sqlite:///database.db")

engine = create_engine(database_name)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_session():
    Base.metadata.create_all(bind=engine)
    try:
        session = SessionLocal()
        yield session
    finally:
        session.close()
