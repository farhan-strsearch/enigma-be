from app.repositories.construction_repository import ConstructionRepository


class ConstructionService:
    def __init__(self, repository: ConstructionRepository):
        self.repository = repository
