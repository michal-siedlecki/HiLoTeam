"""Start serving the application by command
`uvicorn remote_server:app --reload`
for local testing first run mongodb locally
docker run -d -p 27017:27017 --name hilo-mongo mongo:latest
mongo "mongodb://localhost:27017"
"""
import os
import bcrypt
import requests
from bson.objectid import ObjectId as BsonObjectId
from typing import Annotated, Optional
from pydantic import BaseModel
from fastapi import Depends, FastAPI, HTTPException, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi.responses import FileResponse

from starlette import status

from pymongo import MongoClient

from core.rsa_keygen import generate_keys

APP_SECRET_KEY = os.getenv("SECRET_KEY")
DATABASE_URL = os.getenv("DATABASE_URL")
IOT_BASE_IMAGE_PATH = os.getenv("IOT_BASE_IMAGE_PATH")
DEBUG = bool(int(os.getenv("DEBUG")))


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
    debug=DEBUG,
)


def db_context():
    DB_CONNECTION = MongoClient(DATABASE_URL)
    COLLECTION = DB_CONNECTION.users["users"]
    return COLLECTION


@app.get("/panel")
def remote_panel(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    COLLECTION=Depends(db_context),
):
    """User logins, the keys pair is created, the public key is saved in the catalog,
    user downloads the raspberry custom build image and the private key
    """

    result = COLLECTION.find_one({"name": credentials.username})
    if not result:
        raise HTTPException(status_code=403, detail="Forbidden")
    password_plain = credentials.password
    password_hash = result["password"]
    pwd_match = bcrypt.checkpw(password_plain.encode(), password_hash)
    if pwd_match and not result["has_key"]:
        priv, pub = generate_keys()
        name = result["name"]
        save_key(name, pub)
        set_user_has_key(name)
        path = create_custom_image(priv, IOT_BASE_IMAGE_PATH)
        return FileResponse(path)

    if pwd_match and result["has_key"]:
        status_response = requests.get("https://martaclose.hi-lo.pl")
        status_code = status_response.status_code
        return {"status połaczenia": f"{status_code}"}
    raise HTTPException(status_code=403, detail="Forbidden")


class PydanticObjectId(BsonObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not isinstance(v, BsonObjectId):
            raise TypeError("ObjectId required")
        return str(v)


class UserModel(BaseModel):
    name: str
    password: str
    has_key: Optional[bool] = False
    _id: Optional[PydanticObjectId]


@app.get("/users", response_model=list[UserModel])
def get_users(db=Depends(db_context)):
    """Get list of users"""
    users = list(db.find())
    return users


@app.post("/users")
def get_users(user: UserModel, db=Depends(db_context)):
    """Create new user in database"""
    hashed_pwd = bcrypt.hashpw(user.password.encode(), bcrypt.gensalt())
    db.insert_one({"name": user.name, "password": hashed_pwd, "has_key": False})
    # Create user in system
    # os.system(f'adduser --disabled-password --gecos GECOS {name} && sudo su - {name} && mkdir .ssh/')
    # os.chmod(f'/home/{name}/.ssh/authorized_keys', 600)
    # os.chmod(f'/home/{name}/.ssh', 700)
    return status.HTTP_201_CREATED


def create_custom_image(private_key, image_path):
    path = f"./keys/id_rsa"
    with open(f"{path}", "w") as f:
        f.write(private_key)
    return path


def save_key(name, pub):
    # with open(f"/home/{name}/.ssh/authorized_keys", "w") as f:
    path = f"./keys/{name}_id_rsa.pub"
    with open(f"{path}", "w") as f:
        f.write(pub)


def set_user_has_key(name):
    COLLECTION = db_context()
    result = COLLECTION.find_one({"name": name})
    id = result["_id"]
    COLLECTION.update_one(
        {"_id": id},
        {"$set": {"has_key": True}},
    )
