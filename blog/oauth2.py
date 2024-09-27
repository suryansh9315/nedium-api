from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer
from typing import Annotated
from . import hashing

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    return hashing.verify_access_token(token)


