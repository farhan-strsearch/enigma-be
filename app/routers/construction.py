from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.construction_controller import (
    ConstructionAmenitiesController,
    ConstructionRemodelingController,
)
from app.core.database import get_db
from app.repositories.construction_repository import (
    ConstructionAmenitiesRepository,
    ConstructionRemodelingRepository,
)
from app.schemas.construction import (
    ConstructionCostsAmenitiesCreateSchema,
    ConstructionCostsAmenitiesUpdateSchema,
    ConstructionCostsRemodelingCreateSchema,
    ConstructionCostsRemodelingUpdateSchema,
)
from app.services.construction_service import (
    ConstructionAmenitiesService,
    ConstructionRemodelingService,
)

router = APIRouter(prefix="/construction", tags=["construction"])


def get_amenities_controller(db: AsyncSession = Depends(get_db)) -> ConstructionAmenitiesController:
    return ConstructionAmenitiesController(ConstructionAmenitiesService(ConstructionAmenitiesRepository(db)))


def get_remodeling_controller(db: AsyncSession = Depends(get_db)) -> ConstructionRemodelingController:
    return ConstructionRemodelingController(ConstructionRemodelingService(ConstructionRemodelingRepository(db)))


# --- Amenities ---

@router.get("/amenities/")
async def get_all_amenities(
    location: str | None = Query(None),
    search: str | None = Query(None),
    controller: ConstructionAmenitiesController = Depends(get_amenities_controller),
):
    return await controller.get_all(location=location, search=search)


@router.get("/amenities/{record_id}")
async def get_amenity_by_id(
    record_id: int,
    controller: ConstructionAmenitiesController = Depends(get_amenities_controller),
):
    return await controller.get_by_id(record_id)


@router.post("/amenities/", status_code=201)
async def create_amenity(
    data: ConstructionCostsAmenitiesCreateSchema,
    controller: ConstructionAmenitiesController = Depends(get_amenities_controller),
):
    return await controller.create(data)


@router.patch("/amenities/{record_id}")
async def update_amenity(
    record_id: int,
    data: ConstructionCostsAmenitiesUpdateSchema,
    controller: ConstructionAmenitiesController = Depends(get_amenities_controller),
):
    return await controller.update(record_id, data)


@router.delete("/amenities/{record_id}")
async def delete_amenity(
    record_id: int,
    controller: ConstructionAmenitiesController = Depends(get_amenities_controller),
):
    return await controller.delete(record_id)


# --- Remodeling ---

@router.get("/remodeling/")
async def get_all_remodeling(
    location: str | None = Query(None),
    search: str | None = Query(None),
    controller: ConstructionRemodelingController = Depends(get_remodeling_controller),
):
    return await controller.get_all(location=location, search=search)


@router.get("/remodeling/{record_id}")
async def get_remodeling_by_id(
    record_id: int,
    controller: ConstructionRemodelingController = Depends(get_remodeling_controller),
):
    return await controller.get_by_id(record_id)


@router.post("/remodeling/", status_code=201)
async def create_remodeling(
    data: ConstructionCostsRemodelingCreateSchema,
    controller: ConstructionRemodelingController = Depends(get_remodeling_controller),
):
    return await controller.create(data)


@router.patch("/remodeling/{record_id}")
async def update_remodeling(
    record_id: int,
    data: ConstructionCostsRemodelingUpdateSchema,
    controller: ConstructionRemodelingController = Depends(get_remodeling_controller),
):
    return await controller.update(record_id, data)


@router.delete("/remodeling/{record_id}")
async def delete_remodeling(
    record_id: int,
    controller: ConstructionRemodelingController = Depends(get_remodeling_controller),
):
    return await controller.delete(record_id)
