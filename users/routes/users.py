from fastapi import APIRouter, Depends
from users.models import User
from users.handler import UserHandler
from dependencies import authentication

router = APIRouter()


@router.get("/get_user_details", name="get_user_details")
async def get_user_details(user_id: str):
    user_handler = UserHandler()
    user = user_handler.get_fs_user(user_id)
    return user.__dict__


@router.get("/get_current_user_details", name="get_current_user_details")
async def get_current_user_details(user: User = Depends(authentication.get_current_user_authorizer())):
    user_handler = UserHandler()
    user = user_handler.get_fs_user(user.uid)
    return user.__dict__


@router.patch("/disable", name="disable_current_user")
async def disable_current_user(user: User = Depends(authentication.get_current_user_authorizer())):
    UserHandler.disable_user(user.uid)
    return {"status": "user disabled successfully"}
