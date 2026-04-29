import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.opex import OpexBySize

OPEX_BY_SIZE = [
    # Market 1 — Nashville
    {"market_id":1, "sqft": 1000, "internet": 100, "pest_control": 60, "utilities": 400},
    {"market_id":1, "sqft": 1500, "internet": 100, "pest_control": 60, "utilities": 500},
    {"market_id":1, "sqft": 2000, "internet": 100, "pest_control": 60, "utilities": 600},
    {"market_id":1, "sqft": 2750, "internet": 150, "pest_control": 75, "utilities": 700},
    {"market_id":1, "sqft": 3500, "internet": 150, "pest_control": 75, "utilities": 800},
    {"market_id":1, "sqft": 4500, "internet": 150, "pest_control": 75, "utilities": 900},
    # Market 2 — Scottsdale
    {"market_id":2, "sqft": 1000, "internet": 100, "pest_control": 60, "utilities": 425},
    {"market_id":2, "sqft": 1500, "internet": 100, "pest_control": 60, "utilities": 525},
    {"market_id":2, "sqft": 2000, "internet": 100, "pest_control": 60, "utilities": 600},
    {"market_id":2, "sqft": 2750, "internet": 150, "pest_control": 75, "utilities": 675},
    {"market_id":2, "sqft": 3500, "internet": 150, "pest_control": 75, "utilities": 750},
    {"market_id":2, "sqft": 4500, "internet": 150, "pest_control": 75, "utilities": 850},
    # Market 3 — Miami
    {"market_id":3, "sqft": 1000, "internet": 100, "pest_control": 60, "utilities": 350},
    {"market_id":3, "sqft": 1500, "internet": 100, "pest_control": 60, "utilities": 425},
    {"market_id":3, "sqft": 2000, "internet": 100, "pest_control": 60, "utilities": 500},
    {"market_id":3, "sqft": 2750, "internet": 150, "pest_control": 75, "utilities": 600},
    {"market_id":3, "sqft": 3500, "internet": 150, "pest_control": 75, "utilities": 700},
    {"market_id":3, "sqft": 4500, "internet": 150, "pest_control": 75, "utilities": 800},
]


async def seed():
    async with AsyncSessionLocal() as session:
        existing = (await session.execute(select(OpexBySize))).scalars().all()
        existing_keys = {(r.market_id, r.sqft) for r in existing}

        to_insert = [
            OpexBySize(**row)
            for row in OPEX_BY_SIZE
            if (row["market_id"], row["sqft"]) not in existing_keys
        ]

        if not to_insert:
            print("Nothing to seed — all opex_by_size records already exist.")
            return

        session.add_all(to_insert)
        await session.commit()
        print(f"Seeded {len(to_insert)} opex_by_size record(s).")


if __name__ == "__main__":
    asyncio.run(seed())
