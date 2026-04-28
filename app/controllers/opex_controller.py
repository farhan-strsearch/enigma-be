from app.services.opex_service import OpexService


class OpexController:
    def __init__(self, service: OpexService):
        self.service = service
