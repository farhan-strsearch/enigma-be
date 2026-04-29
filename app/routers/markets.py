from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.market_controller import MarketController
from app.core.database import get_db
from app.repositories.market_repository import MarketRepository
from app.schemas.market import MarketCreateSchema, MarketUpdateSchema
from app.services.market_service import MarketService

router = APIRouter(prefix="/markets", tags=["markets"])


def get_controller(db: AsyncSession = Depends(get_db)) -> MarketController:
    return MarketController(MarketService(MarketRepository(db)))


@router.get("/")
async def get_paginated(
    page: int = Query(1, ge=1),
    page_size: int = Query(20, ge=1, le=100),
    market_status: str | None = Query(None),
    analyst_owner: str | None = Query(None),
    search: str | None = Query(None),
    controller: MarketController = Depends(get_controller),
):
    return await controller.get_paginated(
        page=page,
        page_size=page_size,
        market_status=market_status,
        analyst_owner=analyst_owner,
        search=search,
    )


@router.get("/slug/{market_slug}")
async def get_by_market_slug(
    market_slug: str,
    controller: MarketController = Depends(get_controller),
):
    return await controller.get_by_market_slug(market_slug)


@router.get("/{market_id}")
async def get_by_id(
    market_id: int,
    controller: MarketController = Depends(get_controller),
):
    return await controller.get_by_id(market_id)


@router.post("/", status_code=201)
async def create(
    data: MarketCreateSchema,
    controller: MarketController = Depends(get_controller),
):
    return await controller.create(data)


@router.patch("/{market_id}")
async def update(
    market_id: int,
    data: MarketUpdateSchema,
    controller: MarketController = Depends(get_controller),
):
    return await controller.update(market_id, data)


@router.delete("/{market_id}")
async def delete(
    market_id: int,
    controller: MarketController = Depends(get_controller),
):
    return await controller.delete(market_id)

