from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.opex_controller import OpexByBedroomsController, OpexBySizeController
from app.core.database import get_db
from app.repositories.market_repository import MarketRepository
from app.repositories.opex_repository import OpexByBedroomsRepository, OpexBySizeRepository
from app.schemas.opex import (
    OpexByBedroomsCreateSchema,
    OpexByBedroomsUpdateSchema,
    OpexBySizeCreateSchema,
    OpexBySizeUpdateSchema,
)
from app.services.opex_service import OpexByBedroomsService, OpexBySizeService

router = APIRouter(prefix="/opex", tags=["opex"])


def get_bedrooms_controller(db: AsyncSession = Depends(get_db)) -> OpexByBedroomsController:
    market_repo = MarketRepository(db)
    return OpexByBedroomsController(OpexByBedroomsService(OpexByBedroomsRepository(db), market_repo))


def get_size_controller(db: AsyncSession = Depends(get_db)) -> OpexBySizeController:
    market_repo = MarketRepository(db)
    return OpexBySizeController(OpexBySizeService(OpexBySizeRepository(db), market_repo))


# --- By Bedrooms ---

@router.get("/bedrooms/")
async def get_bedrooms_paginated(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    market_id: int | None = Query(None),
    market_slug: str | None = Query(None),
    bedrooms: int | None = Query(None),
    controller: OpexByBedroomsController = Depends(get_bedrooms_controller),
):
    return await controller.get_paginated(
        page=page,
        page_size=page_size,
        market_id=market_id,
        market_slug=market_slug,
        bedrooms=bedrooms,
    )


@router.get("/bedrooms/{record_id}")
async def get_bedrooms_by_id(
    record_id: int,
    controller: OpexByBedroomsController = Depends(get_bedrooms_controller),
):
    return await controller.get_by_id(record_id)


@router.post("/bedrooms/", status_code=201)
async def create_bedrooms(
    data: OpexByBedroomsCreateSchema,
    controller: OpexByBedroomsController = Depends(get_bedrooms_controller),
):
    return await controller.create(data)


@router.patch("/bedrooms/{record_id}")
async def update_bedrooms(
    record_id: int,
    data: OpexByBedroomsUpdateSchema,
    controller: OpexByBedroomsController = Depends(get_bedrooms_controller),
):
    return await controller.update(record_id, data)


@router.delete("/bedrooms/{record_id}")
async def delete_bedrooms(
    record_id: int,
    controller: OpexByBedroomsController = Depends(get_bedrooms_controller),
):
    return await controller.delete(record_id)


# --- By Size ---

@router.get("/size/")
async def get_size_paginated(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    market_id: int | None = Query(None),
    market_slug: str | None = Query(None),
    sqft: int | None = Query(None),
    controller: OpexBySizeController = Depends(get_size_controller),
):
    return await controller.get_paginated(
        page=page,
        page_size=page_size,
        market_id=market_id,
        market_slug=market_slug,
        sqft=sqft,
    )


@router.get("/size/{record_id}")
async def get_size_by_id(
    record_id: int,
    controller: OpexBySizeController = Depends(get_size_controller),
):
    return await controller.get_by_id(record_id)


@router.post("/size/", status_code=201)
async def create_size(
    data: OpexBySizeCreateSchema,
    controller: OpexBySizeController = Depends(get_size_controller),
):
    return await controller.create(data)


@router.patch("/size/{record_id}")
async def update_size(
    record_id: int,
    data: OpexBySizeUpdateSchema,
    controller: OpexBySizeController = Depends(get_size_controller),
):
    return await controller.update(record_id, data)


@router.delete("/size/{record_id}")
async def delete_size(
    record_id: int,
    controller: OpexBySizeController = Depends(get_size_controller),
):
    return await controller.delete(record_id)
