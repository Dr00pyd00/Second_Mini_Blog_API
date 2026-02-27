from calendar import c

import pytest

from fastapi.testclient import TestClient
from sqlalchemy.orm import Session, sessionmaker
from sqlalchemy import create_engine

from app.main import app
from app.core.databse import Base
from app.dependencies.database import get_db


# create fictive db:
SQL_URL_FAKE = "sqlite:///./test.db"

test_engine = create_engine(
    url=SQL_URL_FAKE,
    connect_args={"check_same_thread":False}
    )

TestSessionLocal = sessionmaker(
    bind=test_engine,
    autocommit=False,
    autoflush=False,
)


# mixtures : func who run before each test_func

# get a db :
@pytest.fixture(scope="function")
def db_session():
    # create all tables
    Base.metadata.create_all(bind=test_engine)

    # one session 
    db = TestSessionLocal()

    # make generator
    try:
        yield db
    finally:
        # delete data
        Base.metadata.drop_all(bind=test_engine)
        # close AFTER
        db.close()
    

# get a client :
@pytest.fixture(scope="function")
def client(db_session:Session):

    # func who gonna override get_db
    def get_db_override():
        try:
            yield db_session
        finally:
            pass # in the db_session func continue
    
    # override 
    app.dependency_overrides[get_db] = get_db_override

    # give app like if we gived to Uvicorn to server
    yield TestClient(app) 

    # cancel all overrides:
    app.dependency_overrides.clear()



# prepare some preset users ======================================================

# auto creation user
@pytest.fixture
def create_user(client: TestClient):

    user_data = {
        "username":"testuser",
        "password":"test123"
    }
    response = client.post("users", json=user_data)
    return response

# auto login user : return the access_token
@pytest.fixture
def auth_token(client: TestClient, create_user):

    user_data = {
        "username":"testuser",
        "password":"test123"
    }
    response = client.post("login", data=user_data)

    return response.json()["access_token"]

#  get the good header form
@pytest.fixture
def auth_header(auth_token):
    return {"Authorization":f"Bearer {auth_token}"}
 


 
