from typing import List

from fastapi import HTTPException, status

# from fastapi.responses import JSONResponse
from sqlalchemy.orm import Session

# from utils.helpers import UserDict
from src.schemas import schemas
from src.models import models

from src.repositories.repos import UserRepo


class OrganisationService:
    def create_user_organisation(
        self, db: Session, organisation: schemas.OrganisationCreate, user: models.User
    ) -> models.Organisation | None:
        repo = UserRepo()

        existing_org = repo.get_organisation_by_email(db, organisation.email)

        if existing_org:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Organisation with email {organisation.email} already exists",
            )

        user_organisation_create_payload = schemas.OrganisationCreate(
            name=f"{user.firstname}'s organisation",
            email=user.email,
        )
        # new_user_organisation = schemas.OrganisationCreate(
        #     name=f"{user.firstname}'s organisation",
        #     email=new_user.email.value,
        # )

        user_org = repo.create_user_organisation(db, user_organisation_create_payload)

        repo.insert_user_organisation_association(
            db, user.user_id, user_org.organisation_id, roles=schemas.UserRoles.USER
        )

    def get_organisations(
        self, db: Session, skip: int = 0, limit: int = 100
    ) -> List[models.Organisation]:
        return db.query(models.Organisation).limit(limit).offset(skip).all()


organisation_service = OrganisationService()
