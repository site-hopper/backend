from fastapi import FastAPI, Request, Depends, APIRouter
import firebase_admin
from fastapi.openapi.models import Response
from firebase_admin import credentials
from firebase_admin import auth

from comments.handler import CommentHandler
from comments.models import CommentFS
from models import NewComment, NewReply, UpdateComment
from users.models import User
from dependencies import authentication

router = APIRouter()



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




@router.get("/api/v1/comment")
def get_comments(domain: str, route: str):
    route = route.replace("/", "::")
    comment_handler = CommentHandler(domain, route)
    list_comment = comment_handler.get_all_comment()
    return list_comment


@router.post("/api/v1/comment")
def add_comment(icomment: NewComment, user: User = Depends(authentication.get_current_user_authorizer())):
    comment_handler = CommentHandler(icomment.domain, icomment.route)
    comment_handler.add_comment(icomment)

    return {"status":"Comment Added successfully"}


@router.post("/api/v1/reply")
def add_reply(icomment: NewReply, user: User = Depends(authentication.get_current_user_authorizer())):
    comment_handler = CommentHandler(icomment.domain, icomment.route)
    comment_handler.add_reply(icomment)

    return {"status": "Comment Added successfully"}


@router.patch("/api/v1/comment")
def update_comment(icomment: UpdateComment, user: User = Depends(authentication.get_current_user_authorizer())):
    comment_handler = CommentHandler(icomment.domain, icomment.route)

    # create firestore comment object and update
    # TODO: add reference to user
    comment_handler.add_comment(UpdateComment)





