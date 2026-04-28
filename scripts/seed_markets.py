import asyncio
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parent.parent))

from sqlalchemy import select
from app.core.database import AsyncSessionLocal
from app.models.market import MarketKeysMaster

MARKETS = [
    {
        "market_slug": "nashville-tn",
        "market_name": "Nashville, TN",
        "market_name_current": "Nashville",
        "market_status": "active",
        "analyst_owner": "",
    },
    {
        "market_slug": "scottsdale-az",
        "market_name": "Scottsdale, AZ",
        "market_name_current": "Scottsdale",
        "market_status": "active",
        "analyst_owner": "",
    },
    {
        "market_slug": "miami-fl",
        "market_name": "Miami, FL",
        "market_name_current": "Miami",
        "market_status": "active",
        "analyst_owner": "",
    },
]


async def seed():
    async with AsyncSessionLocal() as session:
        existing = (await session.execute(select(MarketKeysMaster))).scalars().all()
        existing_slugs = {m.market_slug for m in existing}

        to_insert = [
            MarketKeysMaster(**m)
            for m in MARKETS
            if m["market_slug"] not in existing_slugs
        ]

        if not to_insert:
            print("Nothing to seed — all markets already exist.")
            return

        session.add_all(to_insert)
        await session.commit()
        print(f"Seeded {len(to_insert)} market(s):")
        for m in to_insert:
            print(f"  {m.market_slug}")


if __name__ == "__main__":
    asyncio.run(seed())
