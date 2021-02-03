from fastapi import FastAPI
from fastapi.exceptions import RequestValidationError
from starlette.exceptions import HTTPException
from starlette.middleware.cors import CORSMiddleware

from app.api.routes.api import router
from app.core.config import PROJECT_NAME, DEBUG, VERSION, ALLOWED_HOSTS, API_PREFIX
from app.core.events import create_start_app_handler


def get_application() -> FastAPI:
    application = FastAPI(title=PROJECT_NAME, debug=DEBUG, version=VERSION)
    application.add_middleware(
        CORSMiddleware, allow_origins=ALLOWED_HOSTS or ["*"], allow_credentials=True, allow_methods=["*"],
        allow_headers=["*"])
    application.add_event_handler("startup", create_start_app_handler(application))
    application.add_event_handler("shutdown", create_start_app_handler(application))
    application.add_exception_handler(HTTPException, http_error_handler)
    application.add_exception_handler(RequestValidationError, http422_error_handler)
    application.include_router(router, prefix=API_PREFIX)
    return application


app = get_application()
