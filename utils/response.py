from typing import Any

from fastapi.responses import JSONResponse


def create_response(
    message: str,
    status_code: int,
    access_token: str | None = None,
    data: dict[str, str] | None = None,
    success: bool | None = None,
):
    """Returns a generic JSON Response"""

    response_data: dict[str, str | int | bool | dict[str, Any]] = {
        "status_code": status_code,
        "message": message,
    }

    if data is not None:
        response_data["data"] = data

    if success is not None:
        response_data["success"] = success

    if access_token is not None:
        response_data["access_token"] = access_token

    return response_data


def fail_response(status_code: int, message: str, data: dict[str, str] | None = None):
    return JSONResponse(
        create_response(status_code=status_code, message=message, success=False)
    )


def success_response(data: dict[str, Any], message: str, status_code: int):
    return JSONResponse(
        create_response(
            data=data, message=message, status_code=status_code, success=True
        )
    )


def auth_response(
    access_token: str, data: dict[str, Any], message: str, status_code: int
):
    return JSONResponse(
        create_response(
            access_token=access_token,
            data=data,
            message=message,
            status_code=status_code,
        )
    )
