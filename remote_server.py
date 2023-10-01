"""Start serving the application by command
`uvicorn remote_server:app --reload`
for local testing first run mongodb locally
docker run -d -p 27017:27017 --name hilo-mongo mongo:latest
"""
import bcrypt
import requests
from typing import Annotated
from fastapi import Depends, FastAPI, HTTPException, Form, Request
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from pymongo import MongoClient

TEMPLATES = Jinja2Templates(directory="templates")
APP_SECRET_KEY = "1234"
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

app.mount("/static", StaticFiles(directory="static"), name="static")


@app.get("/panel")
def remote_panel(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)], request: Request
):
    """User login for remote panel"""

    result = COLLECTION.find_one({"name": credentials.username})
    if not result:
        raise HTTPException(status_code=403, detail="Forbidden")
    password_plain = credentials.password
    password_hash = result["password"]
    pwd_match = bcrypt.checkpw(password_plain.encode(), password_hash)
    if pwd_match and not result["has_key"]:
        name = result["name"]
        return TEMPLATES.TemplateResponse(
            "public_key_input.html", {"request": request, "name": name}
        )
    if pwd_match and result["has_key"]:
        name = result["name"]
        status_response = requests.get('https://martaclose.hi-lo.pl')
        with open(f'/home/{name}/.ssh/authorized_keys') as file:
            public_key = file.read()
        status_response = requests.get("https://martaclose.hi-lo.pl")
        status_code = status_response.status_code
        return TEMPLATES.TemplateResponse(
            "status_template.html", {"request": request, "name": name, "status_code": status_code, "public_key": public_key}
        )
    raise HTTPException(status_code=403, detail="Forbidden")


def is_valid_key(text: str):
    return True


@app.post("/panel")
def remote_panel(
    credentials: Annotated[HTTPBasicCredentials, Depends(security)],
    key_text: str = Form(),
):
    """User post public key to the remote server"""
    if not is_valid_key(key_text):
        raise HTTPException(status_code=422, detail="Unprocessable entry")
    name = credentials.username
    # with open(f"/home/{name}/.ssh/authorized_keys", "w") as f:
    with open(f"{name}_id_rsa.pub", "w") as f:  # local dev
        f.write(key_text)
    result = COLLECTION.find_one({"name": name})
    id = result["_id"]
    COLLECTION.update_one(
        {"_id": id},
        {"$set": {"has_key": "1"}},
    )

    return status.HTTP_201_CREATED
