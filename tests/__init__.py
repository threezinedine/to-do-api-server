import os
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from databases.base import Base


testing_database_name = os.getenv("TEST_DATABASE_URL", "sqlite:///testingdatabase.db")

testing_engine = create_engine(testing_database_name)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=testing_engine)

def get_testing_session():
    Base.metadata.create_all(bind=testing_engine)
    try:
        session = TestingSessionLocal()
        yield session
    finally:
        session.close()

from tests.api.v1 import *
from tests.controllers import *
