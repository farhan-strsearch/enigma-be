from app.repositories.opex_repository import OpexRepository


class OpexService:
    def __init__(self, repository: OpexRepository):
        self.repository = repository
