from fastapi import APIRouter

from routes import comments, authentication, users

router = APIRouter()

router.include_router(comments.router)
router.include_router(authentication.router, prefix="/auth")
router.include_router(users.router, prefix="/users")
