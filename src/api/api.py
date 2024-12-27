from fastapi import APIRouter

# from api.routes import organisations
from src.api.routes.users import users_router
from src.api.routes.auth import auth_router
from src.api.routes.organisations import organisations_router

router = APIRouter(prefix="/api")

router.include_router(auth_router)
router.include_router(organisations_router)
router.include_router(users_router)
