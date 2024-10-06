from fastapi import APIRouter

from .user import router as user_router
from .note import router as note_router
from .tg_profile import router as tg_profile_router
from .auth import router as auth_router


router = APIRouter(prefix="/v1")
router.include_router(user_router)
router.include_router(note_router)
router.include_router(tg_profile_router)
router.include_router(auth_router)
