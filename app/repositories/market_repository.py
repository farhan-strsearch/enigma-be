from sqlalchemy.ext.asyncio import AsyncSession


class MarketRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
