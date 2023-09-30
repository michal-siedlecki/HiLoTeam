"""Start serving the application by command
`uvicorn remote_server:app --reload`
"""
import os
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Database which persists users and passwords for remote login
DATABASE_URL = os.getenv('DATABASE_URL')
APP_SECRET_KEY = os.getenv('APP_SECRET_KEY')

# Create database or connect to existing one
engine = create_engine(DATABASE_URL)
session_local = sessionmaker(autocommit=False, autoflush=False, bind=engine)
BaseModel = declarative_base()

BaseModel.metadata.create_all(bind=engine)


security = HTTPBasic()

database = {"adam": "1234", "janina": "1234", "sławek": "1234"}


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


@app.get("/", status_code=status.HTTP_200_OK)
def remote_panel(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    """User login for remote panel"""
    user = credentials.username
    if user not in database.keys():
        return status.HTTP_403_FORBIDDEN
    if database.get(user) == credentials.password:
        return {f"Welcome {user} to remote panel"}
    return status.HTTP_403_FORBIDDEN

@app.get("/key", status_code=status.HTTP_200_OK)
def remote_panel(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    """User login for remote panel"""
    user = credentials.username
    if user not in database.keys():
        return status.HTTP_403_FORBIDDEN
    if database.get(user) == credentials.password:
        return {f"Welcome {user} to remote panel"}
    return status.HTTP_403_FORBIDDEN
