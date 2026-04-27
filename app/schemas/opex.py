from decimal import Decimal

from app.schemas.common import BaseResponse


class OpexByBedroomsSchema(BaseResponse):
    id: int
    market: int | None = None
    bedrooms: int | None = None
    pool_hot_tub_low: Decimal | None = None
    pool_hot_tub_high: Decimal | None = None
    outdoor_landscaping: Decimal | None = None
    software: Decimal | None = None
    insurance_hoi: Decimal | None = None
    supplies: Decimal | None = None
    capex_reserve: Decimal | None = None
    cleaning_fee: Decimal | None = None
    num_of_turns: int | None = None
    property_taxes: Decimal | None = None
    land_value: Decimal | None = None
    appreciation: Decimal | None = None
    hoa_fees: Decimal | None = None
    furnishings_low: Decimal | None = None
    furnishings_high: Decimal | None = None
    consolidated_shipping: Decimal | None = None


class OpexBySizeSchema(BaseResponse):
    id: int
    market: int | None = None
    sqft: int | None = None
    internet: Decimal | None = None
    pest_control: Decimal | None = None
    utilities: Decimal | None = None
