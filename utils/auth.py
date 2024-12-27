import os

from datetime import datetime, timedelta, timezone
from typing import Any, Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from src.models.models import User

from src.repositories.repos import UserRepo
from db.database import get_db

load_dotenv()

SECRET_KEY = os.environ.get("SECRET_KEY")  # Change this in production
if SECRET_KEY is None:
    raise Exception("Secret key is not set")
ALGORITHM = os.environ.get("ALGORITHM")
if ALGORITHM is None:
    raise Exception("Algorithm is not set")
access_token_expires_minutes_str = os.environ.get("ACCESS_TOKEN_EXPIRE_MINUTES")
if access_token_expires_minutes_str is not None:
    ACCESS_TOKEN_EXPIRE_MINUTES = int(access_token_expires_minutes_str)
else:
    raise Exception("ACCESS_TOKEN_EXPIRE_MINUTES is not set")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="api/users/login"
)  # the authentication scheme


def hash_password(password: str) -> str:
    """Function to hash a password"""

    hashed_password = pwd_context.hash(secret=password)
    return hashed_password


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def authenticate_user(db: Session, email: str, password: str):
    # user = service.get_user_by_email(db, email)
    repo = UserRepo()
    user = repo.get_user_by_email(db, email)

    if not user or not verify_password(password, str(user.hashed_password)):
        return False
    return user


def create_access_token(
    data: dict[str, Any], expires_delta: Optional[timedelta] = None
):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=ACCESS_TOKEN_EXPIRE_MINUTES
        )
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def get_current_user(
    get_user_fn: User,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme),
) -> User:
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload: dict[str, Any] = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email = payload.get("sub")
        if not email:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    # user = service.get_user_by_email(db, email=email)
    user = get_user_fn(db, email)
    if user is None:
        raise credentials_exception
    return user


# implement verify_access_token, create_access_token and create_refresh_token, verify_refresh_token,refresh_access_token and it should be alone insider the UserService class

# get_current_user() should be in the class and it should only get the user. It would contain the ffg, credentials_exception, token, user

# Create settings file, use settings.ALGORITHMS and settings.SECRET_KEY etc
# bring has_password function here
# Refactor JWT Error and print the the error before raising exception
