import firebase_admin
from fastapi.openapi.models import Response
from firebase_admin import credentials
from firebase_admin import auth

from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from errors.http_error import http_error_handler
from errors.validation_error import http422_error_handler
from routes.api import router as api_router

# from app.core.config import ALLOWED_HOSTS, API_PREFIX, DEBUG, PROJECT_NAME, VERSION


cred = credentials.Certificate("site-hopper-adminsdk.json")
firebase_admin.initialize_app(cred)


def get_application() -> FastAPI:
    application = FastAPI(title="site hopper")

    """application.add_middleware(
        CORSMiddleware,
        allow_origins=ALLOWED_HOSTS or ["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )"""

    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)

    application.include_router(api_router)

    return application


app = get_application()
