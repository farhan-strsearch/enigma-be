from app.repositories.market_repository import MarketRepository


class MarketService:
    def __init__(self, repository: MarketRepository):
        self.repository = repository
