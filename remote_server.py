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
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
# from sqlalchemy import create_engine
# from sqlalchemy.orm import sessionmaker, declarative_base

from pymongo import MongoClient

TEMPLATES = Jinja2Templates(directory='templates')
APP_SECRET_KEY = '1234'
DB_CONNECTION = MongoClient("mongodb://localhost:27017")
COLLECTION = DB_CONNECTION.users["users"]


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

# class User(BaseModel):
#     name: str
#     password: str
#
#
# def user_serializer(user) -> dict:
#     return {"name": user["name"], "password": user["password"]}
#
#
# def users_serializer(users) -> list:
#     return [user_serializer(user) for user in users]


@app.get("/")
def remote_panel(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    """User login for remote panel"""

    result = COLLECTION.find_one({"name": credentials.username})
    if not result:
        raise HTTPException(status_code=403, detail="Forbidden")
    if result['password'] == credentials.password and not result['has_key']:
        name = result['name']
        return TEMPLATES.TemplateResponse('public_key_input.html', {"name": name})
    if result['password'] == credentials.password:
        name = result['name']
        return TEMPLATES.TemplateResponse('public_key_input.html', {"name": name})
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

#
# async def get_status_code(url: str):
#     async with aiohttp.ClientSession() as session:
#         async with session.get(url) as response:
#             return response.status
#
# @app.get('/show_status', response_class=HTMLResponse)
# async def show_status(request: Request):
#     try:
#         status = await get_status_code('https://martaclose.hi-lo.pl/')
#     except:
#         status = 'Not connected'
#     return templates.TemplateResponse('status_template.html', {"request": request, 'status': status})
