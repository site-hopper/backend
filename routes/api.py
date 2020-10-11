from fastapi import APIRouter

from routes import comments,authentication


router = APIRouter()

router.include_router(comments.router)
router.include_router(authentication.router, prefix="/users")