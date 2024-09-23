from fastapi import APIRouter

from app.api.v1.user import router as user_router
from app.api.v1.note import router as note_router
from app.api.v1.tg_profile import router as tg_profile_router


router = APIRouter(prefix="/v1")
router.include_router(user_router)
router.include_router(note_router)
router.include_router(tg_profile_router)
