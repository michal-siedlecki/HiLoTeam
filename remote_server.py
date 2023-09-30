"""Start serving the application by command
`uvicorn remote_server:app --reload`
for local testing first run mongodb locally
docker run -d -p 27017:27017 --name hilo-mongo mongo:latest
"""
from typing import Annotated
from pydantic import BaseModel
from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

from pymongo import MongoClient


APP_SECRET_KEY = '1234'

# Create database or connect to existing one
# engine = create_engine(DATABASE_URL)
# session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
# BaseModel = declarative_base()
#
# BaseModel.metadata.create_all(bind=engine)

database = {"adam": "1234", "janina": "1234", "sławek": "1234"}

db_connection = MongoClient("mongodb://localhost:27017")
collection = db_connection.users["users"]
# collection = db["users"]


security = HTTPBasic()


app = FastAPI(
    title="HiLo",
    secret_key=APP_SECRET_KEY,
    description=__doc__,
    version="0.0.1",
    contact={
        "name": "HiLoTeam",
    },
    license_info={
        "name": "MIT",
    },
)


class User(BaseModel):
    name: str
    password: str


def user_serializer(user) -> dict:
    return {"name": user["name"], "password": user["password"]}


def users_serializer(users) -> list:
    return [user_serializer(user) for user in users]


@app.get("/", status_code=status.HTTP_200_OK)
def remote_panel(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    """User login for remote panel"""

    result = collection.find_one({"name": credentials.username})["name"]
    return {f"Cześć {result}"}


    # if user not in database.keys():
    # if not user not in database.keys():
    #     return status.HTTP_403_FORBIDDEN
    # if database.get(user) == credentials.password:
    #     return {f"Welcome {user} to remote panel"}
    # return status.HTTP_403_FORBIDDEN


@app.get("/key", status_code=status.HTTP_200_OK)
def remote_panel(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    """User login for remote panel"""
    user = credentials.username
    if user not in database.keys():
        return status.HTTP_403_FORBIDDEN
    if database.get(user) == credentials.password:
        return {f"Welcome {user} to remote panel"}
    return status.HTTP_403_FORBIDDEN
