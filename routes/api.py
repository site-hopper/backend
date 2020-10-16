from fastapi import APIRouter

from authentication.routes import authentication
from comments.routes import comments
from users.routes import users

router = APIRouter()

router.include_router(comments.router)
router.include_router(authentication.router, prefix="/auth")
router.include_router(users.router, prefix="/users")
