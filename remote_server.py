"""Start serving the application by command
`uvicorn remote_server:app --reload`
for local testing first run mongodb locally
docker run -d -p 27017:27017 --name hilo-mongo mongo:latest
"""
import os
from typing import Annotated
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, Request
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

class PublicKey(BaseModel):
    key: str

class User(BaseModel):
    name: str
    password: str


def user_serializer(user) -> dict:
    return {"name": user["name"], "password": user["password"]}


def users_serializer(users) -> list:
    return [user_serializer(user) for user in users]


@app.get("/")
def remote_panel(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    """User login for remote panel"""

    result = collection.find_one({"name": credentials.username})
    if not result:
        raise HTTPException(status_code=403, detail="Forbidden")
    if result['password'] == credentials.password:
        name = result['name']
        return {f"Cześć {name}"}
    raise HTTPException(status_code=403, detail="Forbidden")

def is_valid_key(text: str):
    return True


@app.post("/")
def remote_panel(credentials: Annotated[HTTPBasicCredentials, Depends(security)], public_key: PublicKey):
    """User post public key to the remote server"""
    key = public_key.key
    print(key)
    if not is_valid_key(key):
        raise HTTPException(status_code=403, detail="Forbidden")  # Fix the proper response
    name = credentials.username
    with open(f"test_{name}_id_rsa.pub", 'w')as f:
        f.write(key)
    return status.HTTP_201_CREATED


