# from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

# from utils.helpers import UserDict
from src.schemas import schemas
from src.models import models

from src.repositories.repos import UserRepo
from utils import auth


class UserService:
    def create_user(
        self,
        db: Session,
        user_data: schemas.UserCreate,
    ) -> models.User:
        hashed_password = auth.hash_password(password=user_data.password)

        user = user_data.model_dump(by_alias=True)
        user["hashed_password"] = hashed_password
        repo = UserRepo()

        return repo.create_user(db, user)

    # def create_organisation(
    #     self,
    #     db: Session,
    #     organisation: schemas.OrganisationCreate,
    # ):
    #     repo = UserRepo()

    #     # new_user_organisation = schemas.OrganisationCreate(
    #     #     name=f"{user.firstname}'s organisation",
    #     #     email=user.email,
    #     # )

    #     return repo.create_organisation(db, organisation)

    def get_user(self, db: Session, user_id: str) -> models.User | None:
        repo = UserRepo()

        return repo.get_user_by_id(db, user_id)

    def get_user_by_email(self, db: Session, email: str) -> models.User | None:
        repo = UserRepo()

        return repo.get_user_by_email(db, email)

    def get_users(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> list[models.User]:
        repo = UserRepo()

        return repo.get_users(db, skip, limit)


user_service = UserService()
