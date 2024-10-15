from fastapi import APIRouter, Depends, HTTPException, Response

from app.schemas import (
    TgProfileCreate,
    TgProfileResponse,
    TgProfileUpdate,
)
from app.services import TgProfileService
from app.exceptions import (
    TgProfileNotFoundException,
    TgProfileAlreadyExistsException,
    UserNotFoundException,
    UserAlreadyExistsException,
)
from app.dependencies import get_tg_profile_service

router = APIRouter(prefix="/tg_profile", tags=["tg_profile"])


@router.get("/", response_model=list[TgProfileResponse])
async def get_all_tg_profiles(
    tg_profile_service: TgProfileService = Depends(get_tg_profile_service),
):
    return await tg_profile_service.get_all_tg_profiles()


@router.post("/", response_model=TgProfileResponse, status_code=201)
async def create_tg_profile(
    new_profile: TgProfileCreate,
    tg_profile_service: TgProfileService = Depends(get_tg_profile_service),
):
    try:
        return await tg_profile_service.create_tg_profile(new_profile)
    except UserAlreadyExistsException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except UserNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
    except TgProfileAlreadyExistsException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.get("/{tg_id}", response_model=TgProfileResponse)
async def get_tg_profile_by_tg_id(
    tg_id: int,
    tg_profile_service: TgProfileService = Depends(get_tg_profile_service),
):
    try:
        return await tg_profile_service.get_tg_profile_by_tg_id(tg_id)
    except TgProfileNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.put("/", response_model=TgProfileResponse)
async def update_tg_profile(
    update_data: TgProfileUpdate,
    tg_profile_service: TgProfileService = Depends(get_tg_profile_service),
):
    try:
        return await tg_profile_service.update_tg_profile(update_data)
    except TgProfileNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))


@router.delete("/{tg_id}")
async def delete_tg_profile(
    tg_id: int,
    tg_profile_service: TgProfileService = Depends(get_tg_profile_service),
):
    try:
        await tg_profile_service.delete_tg_profile(tg_id)
        return Response(status_code=204)
    except TgProfileNotFoundException as e:
        raise HTTPException(status_code=e.status_code, detail=str(e))
