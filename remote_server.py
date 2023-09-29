"""Start serving the application by command
`uvicorn remote_server:app --reload`
"""
from typing import Annotated

from fastapi import Depends, FastAPI
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from starlette import status

app = FastAPI()

security = HTTPBasic()

database = {
    "adam": "1234",
    "janina": "1234",
    "sławek": "1234"
}


@app.get("/",
         status_code=status.HTTP_200_OK)
def remote_panel(credentials: Annotated[HTTPBasicCredentials, Depends(security)]):
    """User login for remote panel"""
    user = credentials.username
    if user not in database.keys():
        return status.HTTP_403_FORBIDDEN
    if database.get(user) == credentials.password:
        return {"Welcome to remote panel"}
    return status.HTTP_403_FORBIDDEN
