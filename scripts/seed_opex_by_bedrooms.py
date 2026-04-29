import asyncio
import sys
from decimal import Decimal
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.opex import OpexByBedrooms

# property_taxes, land_value, appreciation stored as decimals (e.g. 1% → 0.01)
OPEX_BY_BEDROOMS = [
    # Market 1 — Nashville
    {"market_id":1, "bedrooms": 1, "pool_hot_tub_low": 125, "pool_hot_tub_high": 275, "outdoor_landscaping": 100, "software": 50, "insurance_hoi": 200, "supplies": 125, "capex_reserve": "300.00", "cleaning_fee": "125.00", "num_of_turns": 9, "property_taxes": "0.0100", "land_value": "0.16", "appreciation": "0.0425", "hoa_fees": 0, "furnishings_low": 35000, "furnishings_high": 45000, "consolidated_shipping": 13500},
    {"market_id":1, "bedrooms": 2, "pool_hot_tub_low": 125, "pool_hot_tub_high": 275, "outdoor_landscaping": 100, "software": 50, "insurance_hoi": 200, "supplies": 125, "capex_reserve": "325.00", "cleaning_fee": "150.00", "num_of_turns": 8, "property_taxes": "0.0100", "land_value": "0.16", "appreciation": "0.0425", "hoa_fees": 0, "furnishings_low": 40000, "furnishings_high": 52500, "consolidated_shipping": 13500},
    {"market_id":1, "bedrooms": 3, "pool_hot_tub_low": 125, "pool_hot_tub_high": 275, "outdoor_landscaping": 100, "software": 50, "insurance_hoi": 250, "supplies": 175, "capex_reserve": "350.00", "cleaning_fee": "175.00", "num_of_turns": 7, "property_taxes": "0.0100", "land_value": "0.16", "appreciation": "0.0425", "hoa_fees": 0, "furnishings_low": 55000, "furnishings_high": 62500, "consolidated_shipping": 18225},
    {"market_id":1, "bedrooms": 4, "pool_hot_tub_low": 125, "pool_hot_tub_high": 275, "outdoor_landscaping": 150, "software": 50, "insurance_hoi": 300, "supplies": 205, "capex_reserve": "400.00", "cleaning_fee": "225.00", "num_of_turns": 7, "property_taxes": "0.0100", "land_value": "0.16", "appreciation": "0.0425", "hoa_fees": 0, "furnishings_low": 67500, "furnishings_high": 75000, "consolidated_shipping": 18225},
    {"market_id":1, "bedrooms": 5, "pool_hot_tub_low": 125, "pool_hot_tub_high": 275, "outdoor_landscaping": 150, "software": 50, "insurance_hoi": 350, "supplies": 250, "capex_reserve": "500.00", "cleaning_fee": "275.00", "num_of_turns": 6, "property_taxes": "0.0100", "land_value": "0.16", "appreciation": "0.0425", "hoa_fees": 0, "furnishings_low": 77500, "furnishings_high": 87500, "consolidated_shipping": 21000},
    {"market_id":1, "bedrooms": 6, "pool_hot_tub_low": 125, "pool_hot_tub_high": 275, "outdoor_landscaping": 150, "software": 50, "insurance_hoi": 400, "supplies": 300, "capex_reserve": "600.00", "cleaning_fee": "325.00", "num_of_turns": 5, "property_taxes": "0.0100", "land_value": "0.16", "appreciation": "0.0425", "hoa_fees": 0, "furnishings_low": 90000, "furnishings_high": 105000, "consolidated_shipping": 21000},
    {"market_id":1, "bedrooms": 7, "pool_hot_tub_low": 125, "pool_hot_tub_high": 275, "outdoor_landscaping": 150, "software": 50, "insurance_hoi": 400, "supplies": 330, "capex_reserve": "700.00", "cleaning_fee": "375.00", "num_of_turns": 5, "property_taxes": "0.0100", "land_value": "0.16", "appreciation": "0.0425", "hoa_fees": 0, "furnishings_low": 110000, "furnishings_high": 125000, "consolidated_shipping": 23625},
    # Market 2 — Scottsdale
    {"market_id":2, "bedrooms": 1, "pool_hot_tub_low": 125, "pool_hot_tub_high": 275, "outdoor_landscaping": 125, "software": 50, "insurance_hoi": 200, "supplies": 125, "capex_reserve": "300.00", "cleaning_fee": "125.00", "num_of_turns": 7, "property_taxes": "0.0110", "land_value": "0.16", "appreciation": "0.0425", "hoa_fees": 0, "furnishings_low": 35000, "furnishings_high": 45000, "consolidated_shipping": 13500},
    {"market_id":2, "bedrooms": 2, "pool_hot_tub_low": 125, "pool_hot_tub_high": 275, "outdoor_landscaping": 125, "software": 50, "insurance_hoi": 200, "supplies": 125, "capex_reserve": "325.00", "cleaning_fee": "150.00", "num_of_turns": 7, "property_taxes": "0.0110", "land_value": "0.16", "appreciation": "0.0425", "hoa_fees": 0, "furnishings_low": 40000, "furnishings_high": 52500, "consolidated_shipping": 13500},
    {"market_id":2, "bedrooms": 3, "pool_hot_tub_low": 125, "pool_hot_tub_high": 275, "outdoor_landscaping": 125, "software": 50, "insurance_hoi": 250, "supplies": 175, "capex_reserve": "350.00", "cleaning_fee": "200.00", "num_of_turns": 6, "property_taxes": "0.0110", "land_value": "0.16", "appreciation": "0.0425", "hoa_fees": 0, "furnishings_low": 55000, "furnishings_high": 62500, "consolidated_shipping": 18225},
    {"market_id":2, "bedrooms": 4, "pool_hot_tub_low": 125, "pool_hot_tub_high": 275, "outdoor_landscaping": 125, "software": 50, "insurance_hoi": 300, "supplies": 205, "capex_reserve": "400.00", "cleaning_fee": "250.00", "num_of_turns": 6, "property_taxes": "0.0110", "land_value": "0.16", "appreciation": "0.0425", "hoa_fees": 0, "furnishings_low": 67500, "furnishings_high": 75000, "consolidated_shipping": 18225},
    {"market_id":2, "bedrooms": 5, "pool_hot_tub_low": 125, "pool_hot_tub_high": 275, "outdoor_landscaping": 125, "software": 50, "insurance_hoi": 350, "supplies": 250, "capex_reserve": "500.00", "cleaning_fee": "300.00", "num_of_turns": 5, "property_taxes": "0.0110", "land_value": "0.16", "appreciation": "0.0425", "hoa_fees": 0, "furnishings_low": 77500, "furnishings_high": 87500, "consolidated_shipping": 21000},
    {"market_id":2, "bedrooms": 6, "pool_hot_tub_low": 125, "pool_hot_tub_high": 275, "outdoor_landscaping": 125, "software": 50, "insurance_hoi": 400, "supplies": 300, "capex_reserve": "600.00", "cleaning_fee": "350.00", "num_of_turns": 5, "property_taxes": "0.0110", "land_value": "0.16", "appreciation": "0.0425", "hoa_fees": 0, "furnishings_low": 90000, "furnishings_high": 105000, "consolidated_shipping": 21000},
    {"market_id":2, "bedrooms": 7, "pool_hot_tub_low": 125, "pool_hot_tub_high": 275, "outdoor_landscaping": 125, "software": 50, "insurance_hoi": 400, "supplies": 330, "capex_reserve": "700.00", "cleaning_fee": "400.00", "num_of_turns": 5, "property_taxes": "0.0110", "land_value": "0.16", "appreciation": "0.0425", "hoa_fees": 0, "furnishings_low": 110000, "furnishings_high": 125000, "consolidated_shipping": 23625},
    # Market 3 — Miami
    {"market_id":3, "bedrooms": 1, "pool_hot_tub_low": 125, "pool_hot_tub_high": 275, "outdoor_landscaping": 125, "software": 50, "insurance_hoi": 200, "supplies": 125, "capex_reserve": "300.00", "cleaning_fee": "125.00", "num_of_turns": 9, "property_taxes": "0.0085", "land_value": "0.20", "appreciation": "0.0450", "hoa_fees": 0, "furnishings_low": 35000, "furnishings_high": 45000, "consolidated_shipping": 13500},
    {"market_id":3, "bedrooms": 2, "pool_hot_tub_low": 125, "pool_hot_tub_high": 275, "outdoor_landscaping": 125, "software": 50, "insurance_hoi": 200, "supplies": 125, "capex_reserve": "325.00", "cleaning_fee": "150.00", "num_of_turns": 8, "property_taxes": "0.0085", "land_value": "0.20", "appreciation": "0.0450", "hoa_fees": 0, "furnishings_low": 40000, "furnishings_high": 52500, "consolidated_shipping": 13500},
    {"market_id":3, "bedrooms": 3, "pool_hot_tub_low": 125, "pool_hot_tub_high": 275, "outdoor_landscaping": 125, "software": 50, "insurance_hoi": 250, "supplies": 175, "capex_reserve": "350.00", "cleaning_fee": "175.00", "num_of_turns": 7, "property_taxes": "0.0085", "land_value": "0.20", "appreciation": "0.0450", "hoa_fees": 0, "furnishings_low": 55000, "furnishings_high": 62500, "consolidated_shipping": 18225},
    {"market_id":3, "bedrooms": 4, "pool_hot_tub_low": 125, "pool_hot_tub_high": 275, "outdoor_landscaping": 150, "software": 50, "insurance_hoi": 300, "supplies": 205, "capex_reserve": "400.00", "cleaning_fee": "225.00", "num_of_turns": 7, "property_taxes": "0.0085", "land_value": "0.20", "appreciation": "0.0450", "hoa_fees": 0, "furnishings_low": 67500, "furnishings_high": 75000, "consolidated_shipping": 18225},
    {"market_id":3, "bedrooms": 5, "pool_hot_tub_low": 125, "pool_hot_tub_high": 275, "outdoor_landscaping": 150, "software": 50, "insurance_hoi": 350, "supplies": 250, "capex_reserve": "500.00", "cleaning_fee": "285.00", "num_of_turns": 6, "property_taxes": "0.0085", "land_value": "0.20", "appreciation": "0.0450", "hoa_fees": 0, "furnishings_low": 77500, "furnishings_high": 87500, "consolidated_shipping": 21000},
    {"market_id":3, "bedrooms": 6, "pool_hot_tub_low": 125, "pool_hot_tub_high": 275, "outdoor_landscaping": 150, "software": 50, "insurance_hoi": 425, "supplies": 300, "capex_reserve": "600.00", "cleaning_fee": "325.00", "num_of_turns": 5, "property_taxes": "0.0085", "land_value": "0.20", "appreciation": "0.0450", "hoa_fees": 0, "furnishings_low": 90000, "furnishings_high": 105000, "consolidated_shipping": 21000},
    {"market_id":3, "bedrooms": 7, "pool_hot_tub_low": 125, "pool_hot_tub_high": 275, "outdoor_landscaping": 150, "software": 50, "insurance_hoi": 500, "supplies": 330, "capex_reserve": "700.00", "cleaning_fee": "400.00", "num_of_turns": 5, "property_taxes": "0.0085", "land_value": "0.20", "appreciation": "0.0450", "hoa_fees": 0, "furnishings_low": 110000, "furnishings_high": 125000, "consolidated_shipping": 23625},
]


async def seed():
    async with AsyncSessionLocal() as session:
        existing = (await session.execute(select(OpexByBedrooms))).scalars().all()
        existing_keys = {(r.market_id, r.bedrooms) for r in existing}

        to_insert = [
            OpexByBedrooms(**{**row, "property_taxes": Decimal(row["property_taxes"]), "land_value": Decimal(row["land_value"]), "appreciation": Decimal(row["appreciation"])})
            for row in OPEX_BY_BEDROOMS
            if (row["market_id"], row["bedrooms"]) not in existing_keys
        ]

        if not to_insert:
            print("Nothing to seed — all opex_by_bedrooms records already exist.")
            return

        session.add_all(to_insert)
        await session.commit()
        print(f"Seeded {len(to_insert)} opex_by_bedrooms record(s).")


if __name__ == "__main__":
    asyncio.run(seed())
