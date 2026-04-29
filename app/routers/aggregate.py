from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.controllers.aggregate_controller import AutomatedDealUnderwritingController
from app.core.database import get_db
from app.repositories.construction_repository import (
    ConstructionAmenitiesRepository,
    ConstructionRemodelingRepository,
)
from app.repositories.market_repository import MarketRepository
from app.repositories.opex_repository import OpexByBedroomsRepository, OpexBySizeRepository
from app.schemas.aggregate import UnderwritingQuerySchema
from app.services.aggregate_service import AutomatedDealUnderwritingService
from app.services.construction_service import ConstructionAmenitiesService, ConstructionRemodelingService
from app.services.opex_service import OpexByBedroomsService, OpexBySizeService

router = APIRouter(prefix="/underwriting", tags=["underwriting"])


def get_underwriting_controller(db: AsyncSession = Depends(get_db)) -> AutomatedDealUnderwritingController:
    market_repo = MarketRepository(db)
    service = AutomatedDealUnderwritingService(
        opex_by_bedrooms_service=OpexByBedroomsService(OpexByBedroomsRepository(db), market_repo),
        opex_by_size_service=OpexBySizeService(OpexBySizeRepository(db), market_repo),
        construction_amenities_service=ConstructionAmenitiesService(ConstructionAmenitiesRepository(db)),
        construction_remodeling_service=ConstructionRemodelingService(ConstructionRemodelingRepository(db)),
    )
    return AutomatedDealUnderwritingController(service)


@router.get("/")
async def get_underwriting_data(
    query: UnderwritingQuerySchema = Depends(),
    controller: AutomatedDealUnderwritingController = Depends(get_underwriting_controller),
):
    return await controller.get_underwriting_data(
        bedrooms=query.bedrooms,
        sqft=query.sqft,
        market_id=query.market_id,
        market_slug=query.market_slug,
    )
