from fastapi import FastAPI, Request, status
from fastapi.concurrency import asynccontextmanager


from fastapi.encoders import jsonable_encoder
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse

# from fastapi.concurrency import asynccontextmanager
from src.api.api import router
from db.database import engine
from src.models import models

# Refactor later @ night


@asynccontextmanager
async def lifespan(_: FastAPI):
    models.Base.metadata.create_all(bind=engine)
    yield


app = FastAPI(lifespan=lifespan)


@app.exception_handler(RequestValidationError)
def validation_exception_handler(request: Request, exception: RequestValidationError):
    if request.url.path == "/api/users/register":
        return JSONResponse(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            content=jsonable_encoder(
                {"errors": exception.errors, "body": exception.body}
            ),
        )
    else:
        return JSONResponse(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            content="Internal Server Error",
        )


app.include_router(router)
# app.add_exception_handler(RequestValidationError, validation_exception_handler)


@app.get("/home")
def home():
    return {"message": "index works"}


# @app.get("/")
# def read():
#     return "index works"


# if __name__ == "__main__":
#     database.create_db_and_tables()
