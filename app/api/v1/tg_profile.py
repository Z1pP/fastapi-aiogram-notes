from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.schemas import (
    TgProfileCreate, 
    TgProfileResponse, 
    TgProfileUpdate,
)
from app.services import TgProfileService
from app.exceptions import (
    UserNotFoundException, 
    TgProfileAlreadyExistsException, 
    UserAlreadyExistsException
)

router = APIRouter(prefix="/tg_profile", tags=["tg_profile"])


@router.post("/create", response_model=TgProfileResponse, status_code=201)
async def create_tg_profile(
    new_profile: TgProfileCreate, 
    session: AsyncSession = Depends(get_async_session)
    ):
    tg_profile_service = TgProfileService(session)
    try:
        return await tg_profile_service.create_tg_profile(new_profile)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except UserNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except TgProfileAlreadyExistsException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))