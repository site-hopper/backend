from fastapi import FastAPI, Request
import firebase_admin
from fastapi.openapi.models import Response
from firebase_admin import credentials
from firebase_admin import auth

from comments.handler import CommentHandler
from comments.models import CommentFS
from models import UpdateComment, NewComment, NewReply

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
    route = route.replace("/","::")
    comment_handler = CommentHandler(domain, route)
    list_comment = comment_handler.get_all_comment()
    return list_comment


@app.post("/api/v1/comment")
def add_comment(icomment: NewComment):
    comment_handler = CommentHandler(icomment.domain, icomment.route)
    comment_handler.add_comment(icomment)

    return {"status":"Comment Added successfully"}


@app.post("/api/v1/reply")
def add_reply(icomment: NewReply):
    comment_handler = CommentHandler(icomment.domain, icomment.route)
    comment_handler.add_reply(icomment)

    return {"status":"Comment Added successfully"}


@app.patch("/api/v1/comment")
def update_comment(icomment: UpdateComment):
    comment_handler = CommentHandler(icomment.domain, icomment.route)

    # create firestore comment object and update
    # TODO: add reference to user
    comment_handler.update_comment(UpdateComment)