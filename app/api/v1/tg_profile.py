from fastapi import APIRouter, Depends, HTTPException, Response
from sqlalchemy.ext.asyncio import AsyncSession

from app.database import get_async_session
from app.schemas import (
    TgProfileCreate, 
    TgProfileResponse, 
    TgProfileUpdate,
)
from app.services import TgProfileService
from app.exceptions import *

router = APIRouter(prefix="/tg_profile", tags=["tg_profile"])


@router.get("/", response_model=list[TgProfileResponse])
async def get_all_tg_profiles(
    session: AsyncSession = Depends(get_async_session)
):
    tg_profile_service = TgProfileService(session)
    return await tg_profile_service.get_all_tg_profiles()


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
    

@router.get("/get_by_tg_id/{tg_id}", response_model=TgProfileResponse)
async def get_tg_profile_by_tg_id(
    tg_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    tg_profile_service = TgProfileService(session)
    try:
        return await tg_profile_service.get_tg_profile_by_tg_id(tg_id)
    except TgProfileNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    

@router.put("/update", response_model=TgProfileResponse)
async def update_tg_profile(
    update_data: TgProfileUpdate,
    session: AsyncSession = Depends(get_async_session)
):
    tg_profile_service = TgProfileService(session)
    try:
        return await tg_profile_service.update_tg_profile(update_data)
    except TgProfileNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    

@router.delete("/delete/{tg_id}")
async def delete_tg_profile(
    tg_id: int,
    session: AsyncSession = Depends(get_async_session)
):
    tg_profile_service = TgProfileService(session)
    try:
        await tg_profile_service.delete_tg_profile(tg_id)
        return Response(status_code=204)
    except TgProfileNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))