# from http import HTTPStatus
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

# from fastapi.datastructures import FormData
from fastapi.security import OAuth2PasswordRequestFormStrict

# from utils.helpers import validate_fieldss
from src.models.models import User
from utils import auth
from src.schemas import schemas
from db.database import get_db
from src.services.users import user_service
from src.services.organisations import organisation_service

# from models import models

router = APIRouter(tags=["Authentication"], prefix="/auth")
auth_router = router


@router.post("/register", response_model=None, status_code=status.HTTP_201_CREATED)
def register(
    user_payload: schemas.UserCreate,
    # user_organisation: schemas.OrganisationCreate,
    db: Session = Depends(get_db),
) -> JSONResponse | User:
    # db_user = service.get_user_by_email(db, user_payload.email)
    # if db_user:
    #     raise HTTPException(
    #         status_code=HTTPStatus.BAD_REQUEST, detail="User already exists in database"
    #     )
    # validate_fields(user_payload.model_dump())

    new_user = user_service.create_user(
        db,
        user_payload,
    )
    print(new_user)

    new_organisation = schemas.OrganisationCreate(
        name=f"{user_payload.firstname}'s organisation",
        email=user_payload.email,
    )

    organisation_service.create_user_organisation(db, new_organisation, new_user)

    return new_user

    # return models.User(
    #     firstname="abraham",
    #     lastname="lincoln",
    #     email="ab.linc",
    #     hashed_password="anjakfl",
    #     phone="1234567890",
    #     user_id=1,
    # )

    # return {"user": new_user, "db_user_id": 5}


@router.post("/login", response_model=None, status_code=200)
def login(
    form_data: Annotated[OAuth2PasswordRequestFormStrict, Depends()],
    db: Session = Depends(get_db),
):
    user = auth.authenticate_user(db, form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect email or password",
            headers={"WWW-authenticate": "Bearer"},
        )

    access_token = auth.create_access_token({"sub": user.email})

    # refactor to not return a plain object
    return {"access_token": access_token, "token_type": "bearer"}


# email = db.query(models.User.email).first()
# hashed_password = db.query(models.User).filter(models.User.email == )
# verify_password(password, )
