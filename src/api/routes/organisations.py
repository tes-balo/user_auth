# from http import HTTPStatus
from fastapi import APIRouter, Depends
# Depends, HTTPException

# from utils.auth import pwd_context
from src.services.organisations import organisation_service

from sqlalchemy.orm import Session
from db.database import get_db

# from src.models.models import Organisation
# from src.schemas import schemas
# from sqlalchemy.orm import Session
# from database import get_db
# from models import models


router = APIRouter(tags=["Organisations"], prefix="/organisations")
organisations_router = router


@router.get("/test")
def get_organisations(db: Session = Depends(get_db)):
    return organisation_service.get_organisations(db)
