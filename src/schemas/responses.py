from pydantic import BaseModel


class UserDict(BaseModel):
    user_id: str
    firstname: str
    lastname: str
    email: str
    phone: str


class UserResponse(BaseModel):
    status: str
    message: str
    data: UserDict
