import os
import secrets

from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials

security = HTTPBasic()


def verify_admin(credentials: HTTPBasicCredentials = Depends(security)):
    expected_user = os.getenv("ADMIN_USERNAME", "admin")
    expected_pass = os.getenv("ADMIN_PASSWORD", "admin")

    user_ok = secrets.compare_digest(credentials.username, expected_user)
    pass_ok = secrets.compare_digest(credentials.password, expected_pass)

    if not (user_ok and pass_ok):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Неверный логин или пароль",
            headers={"WWW-Authenticate": "Basic"},
        )

    return credentials.username
