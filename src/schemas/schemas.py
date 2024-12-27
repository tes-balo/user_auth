from datetime import datetime
from enum import Enum
from uuid import UUID
from pydantic import BaseModel, EmailStr, Field


class UserBase(BaseModel):
    firstname: str
    lastname: str
    email: EmailStr
    phone: str
    # user_id: str
    # org_id: str


class UserCreate(UserBase):
    password: str = Field(alias="hashed_password")


class UserOut(UserBase):
    user_id: UUID
    # org_id: str

    class Config:
        orm_mode = True


class OrganisationBase(BaseModel):
    name: str
    description: str | None = None
    email: EmailStr


class OrganisationCreate(OrganisationBase):
    pass


class Organisation(OrganisationBase):
    organisation_id: UUID
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class AllUsersResponse(BaseModel):
    user_id: UUID
    firstname: str
    lastname: str
    email: str
    phone: str


###### ENUMS !SECTION #######


class UserRoles(str, Enum):
    USER = "user"
    ADMIN = "admin"
    GUEST = "guest"
    OWNER = "owner"


class UserOrganisationBase(BaseModel):
    roles: UserRoles


# class UserOrganisationCreate(UserOrganisationBase):
#     user_id: UUID
#     organisation_id: UUID

#     class Config:
#         orm_mode = True


# class UserOrganisation(UserOrganisationBase):
#     pass
