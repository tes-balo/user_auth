# To avoid creating a class at runtime, for type-hinting alone.
from typing import TypedDict

from src.models.models import User


# if TYPE_CHECKING:
# Map the `dict` fields here
class UserDict(TypedDict):
    user: User
    p: str
    db_user_id: int


# VALIDATION

# class UserRegistrationValidation:
#     def __init__(self, user_id: int, firstname: str, lastname: str, email: str, password: str, phone: str):


def validate_fields(dictionary: dict[str, str]):
    for key in dictionary:
        if not dictionary[key]:
            raise ValueError("field must be a string")
    print("objct validated")
