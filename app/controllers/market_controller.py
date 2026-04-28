from app.services.market_service import MarketService


class MarketController:
    def __init__(self, service: MarketService):
        self.service = service
