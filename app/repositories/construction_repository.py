from sqlalchemy.ext.asyncio import AsyncSession


class ConstructionRepository:
    def __init__(self, db: AsyncSession):
        self.db = db
