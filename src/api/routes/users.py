from fastapi import APIRouter, Depends
from fastapi.responses import JSONResponse

from src.models import models
from src.schemas import schemas, responses
from db.database import get_db
from src.services.users import user_service
from sqlalchemy.orm import Session
from utils.auth import get_current_user

router = APIRouter(tags=["Users"], prefix="/users")
users_router = router


# @router.get(
#     "/{id}",
#     response_model=None,
#     status_code=200,
# )
# def get_user(
#     id: str,
#     current_user=Depends(get_current_user),
#     db: Session = Depends(get_db),
# ):
#     user = user_service.get_user(db, id)
#     return responses.UserResponse(
#         status="success",
#         message="User found",
#         data=user,
#     )


# @router.get("/user-record", response_model=None, status_code=200)
# def get_user_record(user: schemas.User = Depends(auth.get_current_user)):


@router.get(
    "",
    response_model=list[responses.UserResponse],
    status_code=200,
)
def get_users(db: Session = Depends(get_db)) -> list[models.User]:
    return user_service.get_users(db)
