from typing import Any
from uuid import UUID

# from uuid import UUID
from fastapi.responses import JSONResponse
from fastapi import status
from sqlalchemy import Uuid
from sqlalchemy.orm import Session

from src.schemas.schemas import OrganisationCreate, UserRoles
from src.models.models import Organisation, User, UserOrganisation


class UserRepo:
    def create_user(
        self,
        db: Session,
        user: dict[str, Any],
    ) -> JSONResponse | User:
        db_user = self.get_user_by_email(db, user["email"])

        if db_user:
            return JSONResponse(
                status_code=status.HTTP_409_CONFLICT,
                content={"message": "User already exists"},
            )

        db_user = User(**user)

        db.add(db_user)
        db.flush()
        db.commit()
        db.refresh(db_user)

        return db_user

    def insert_user_organisation_association(
        self,
        db: Session,
        user_id: Uuid[str],
        organisation_id: Uuid[str],
        roles: UserRoles,
    ):
        user_organisation_association = UserOrganisation.__table__
        stmt = user_organisation_association.insert().values(
            user_id=user_id,
            organisation_id=organisation_id,
            roles=roles,
        )

        db.execute(stmt)
        db.commit()

        return

    def create_user_organisation(
        self,
        db: Session,
        organisation_payload: OrganisationCreate,
    ):
        # new_user_organisation = OrganisationCreate(
        #     name=f"{user.firstname}'s organisation",
        #     email=user.email,
        # )
        organisation = Organisation(**organisation_payload.model_dump())

        db.add(organisation)
        db.commit()
        db.refresh(organisation)

        return organisation

    # return 5

    def get_organisation_by_email(self, db: Session, email: str) -> Organisation | None:
        return db.query(Organisation).filter(Organisation.email == email).first()

    def get_user_by_email(self, db: Session, email: str) -> User | None:
        return db.query(User).filter(User.email == email).first()

    def get_user_by_id(self, db: Session, id: str) -> User | None:
        return db.query(User).filter(User.user_id == UUID(id)).first()

    def get_users(self, db: Session, skip: int = 0, limit: int = 100) -> list[User]:
        return db.query(User).limit(limit).offset(skip).all()


# from typing import List

# from fastapi import status
# from fastapi.responses import JSONResponse
# from sqlalchemy.orm import Session

# # from utils.helpers import UserDict
# from src.schemas import schemas
# from src.models import models
# from utils.auth import pwd_context


# class Services:
#     def create_user(
#         self,
#         db: Session,
#         user: schemas.UserCreate,
#     ):
#         db_user = self.get_user_by_email(db, user.email)

#         if db_user:
#             return JSONResponse(
#                 status_code=status.HTTP_400_BAD_REQUEST,
#                 content={"message": "User already exists"},
#             )

#         hashed_password = pwd_context.hash(user.password)

#         db_user = models.User(
#             firstname=user.firstname,
#             lastname=user.lastname,
#             email=user.email,
#             phone=user.phone,
#             hashed_password=hashed_password,
#         )

#         db.add(db_user)
#         db.flush()
#         db.commit()
#         db.refresh(db_user)

#         return db_user

#     def get_user(self, db: Session, user_id: int) -> models.User | None:
#         return db.query(models.User).filter(models.User.user_id == user_id).first()

#     def get_user_by_email(self, db: Session, email: str) -> models.User | None:
#         return db.query(models.User).filter(models.User.email == email).first()

#     def get_users(
#         self, db: Session, skip: int = 0, limit: int = 100
#     ) -> List[models.User]:
#         return db.query(models.User).limit(limit).offset(skip).all()

#     def create_user_organisation(
#         self, db: Session, organisation: schemas.OrganisationCreate, user: schemas.User
#     ) -> models.Organisation:
#         db_organisation = models.Organisation(
#             name=organisation.name,
#             description=organisation.description,
#             owner_id=user.user_id,
#         )

#         db.add(db_organisation)
#         db.flush()
#         db.commit()
#         db.refresh(db_organisation)

#         return db_organisation

#     def get_organisations(
#         self, db: Session, skip: int = 0, limit: int = 100
#     ) -> List[models.Organisation]:
#         return db.query(models.Organisation).limit(limit).offset(skip).all()


# service = Services()
