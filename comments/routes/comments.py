from fastapi import Depends, APIRouter
from firebase_admin import auth

from comments.handler import CommentHandler
from comments.schema.comments import NewComment, NewReply, UpdateComment
from comments.schema.votes import Vote, RemoveVote
from users.handler import UserHandler
from users.models import User
from dependencies import authentication

router = APIRouter()


@router.get("/api/v1/comment")
def get_comments(domain: str, route: str):
    route = route.replace("/", "::")
    comment_handler = CommentHandler(domain, route)
    list_comment = comment_handler.get_all_comment()
    return list_comment


@router.post("/api/v1/comment")
def add_comment(icomment: NewComment, user: User = Depends(authentication.get_current_user_authorizer())):
    user_handler = UserHandler()
    fs_user = user_handler.get_fs_user(user.uid)
    fs_user.id = user.uid

    comment_handler = CommentHandler(icomment.domain, icomment.route )
    comment_handler.add_comment(icomment, fs_user)

    return {"status":"Comment Added successfully"}


@router.post("/api/v1/reply")
def add_reply(icomment: NewReply, user: User = Depends(authentication.get_current_user_authorizer())):
    user_handler = UserHandler()
    fs_user = user_handler.get_fs_user(user.uid)
    fs_user.id = user.uid
    comment_handler = CommentHandler(icomment.domain, icomment.route)
    comment_handler.add_reply(icomment, fs_user)

    return {"status": "Comment Added successfully"}


@router.patch("/api/v1/comment")
def update_comment(icomment: UpdateComment, user: User = Depends(authentication.get_current_user_authorizer())):
    comment_handler = CommentHandler(icomment.domain, icomment.route)
    comment_handler.add_comment(UpdateComment)


@router.post("/api/v1/vote")
def add_vote(vote: Vote, user: User = Depends(authentication.get_current_user_authorizer())):
    comment_handler = CommentHandler(vote.domain, vote.route)
    comment_handler.add_vote(vote, user)

    return {"status": "Vote Added successfully"}

@router.delete("/api/v1/vote")
def delete_vote(remove_vote: RemoveVote, user: User = Depends(authentication.get_current_user_authorizer())):
    comment_handler = CommentHandler(remove_vote.domain, remove_vote.route)
    comment_handler.remove_vote(remove_vote, user)

    return {"status": "Vote removed successfully"}







