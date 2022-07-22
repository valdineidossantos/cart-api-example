from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.database_helper import Base
from app.main import app, get_db
from fastapi import status

import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)


class TestUser:

    @pytest.mark.asyncio
    async def test_create_users_should_success(self):
        #Then
        payload  = {
            "name": "string",
            "email": "string@string.com",
            "active": "true"
        }
        #When
        response =   client.post("/v1/users/",json=payload)    

        #Then
        assert response.status_code == status.HTTP_201_CREATED, response.text
        data = response.json()
        assert data["email"] == payload["email"]
    @pytest.mark.asyncio
    async def test_create_users_should_unprocessing_entity(self):
        #Then
        payload  = {
            "name": "string",
            "email": "string.string.com",#Wrong email
            "active": "true"
        }
        #When
        response =  client.post("/v1/users/",json=payload)    

        #Then
        assert response.status_code == 422  , response.text
        assert response.json()["detail"][0]['msg'] == "Type a valid email"
            