from fastapi.security import HTTPBasic, HTTPBasicCredentials
from fastapi import Depends, HTTPException, status
import secrets

import settings

security = HTTPBasic()

def validate_credentials(credentials: HTTPBasicCredentials = Depends(security)):
    valid_user = secrets.compare_digest(credentials.username, settings.auth_user)
    valid_pass = secrets.compare_digest(credentials.password, settings.auth_pass)
    if not (valid_user or valid_pass):
        raise HTTPException(
            status_code = status.HTTP_401_UNAUTHORIZED,
            detail = "Incorrect email or password",
            headers = {"WWW-Authenticate": "Basic"},
        )
    return (valid_user and valid_pass)
