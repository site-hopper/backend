"""from fastapi import FastAPI, Request, Depends
import firebase_admin
from fastapi.openapi.model import Response
from firebase_admin import credentials
from firebase_admin import auth

from comments.handler import CommentHandler
from comments.model import CommentFS
from model import UpdateComment, NewComment, NewReply
from users.model import User
from dependencies import authentication

app = FastAPI()
cred = credentials.Certificate("site-hopper-adminsdk.json")
firebase_admin.initialize_app(cred)


# @app.middleware("http")
# async def add_process_time_header(request: Request, call_next):
#     bearer_token_str = request.headers.get("authorization",None)
#     print(bearer_token_str)
#     if bearer_token_str is None:
#         return {"no token"}
#     bearer_token = bearer_token_str.split()[1]
#     uid = auth.get_uid_from_token(bearer_token)
#     print("before")
#     #return uid
#     print(uid)
#     response = await call_next(request)
#     print("after")
#
#     return response

@app.get("/")
async def root():
    # user = auth.get_user_by_email("akshayrgund@gmail.com")
    id_token = auth.sign_in_with_email_and_password("akshayrgund@gmail.com", "Password123", True)
    auth.verify_id_token(id_token)
    return id_token


@app.get("/api/v1/comment")
def get_comments(domain: str, route: str):
    route = route.replace("/", "::")
    comment_handler = CommentHandler(domain, route)
    list_comment = comment_handler.get_all_comment()
    return list_comment


@app.post("/api/v1/comment")
def add_comment(icomment: NewComment, user: User = Depends(authentication.get_current_user_authorizer())):
    comment_handler = CommentHandler(icomment.domain, icomment.route)
    comment_handler.add_comment(icomment)

    return {"status":"Comment Added successfully"}


@app.post("/api/v1/reply")
def add_reply(icomment: NewReply, user: User = Depends(authentication.get_current_user_authorizer())):
    comment_handler = CommentHandler(icomment.domain, icomment.route)
    comment_handler.add_reply(icomment)

    return {"status": "Comment Added successfully"}


@app.patch("/api/v1/comment")
def update_comment(icomment: UpdateComment, user: User = Depends(authentication.get_current_user_authorizer())):
    comment_handler = CommentHandler(icomment.domain, icomment.route)

    # create firestore comment object and update
    # TODO: add reference to user
    comment_handler.add_comment(UpdateComment)





"""

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
