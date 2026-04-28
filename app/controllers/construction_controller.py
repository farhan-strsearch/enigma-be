from app.services.construction_service import ConstructionService


class ConstructionController:
    def __init__(self, service: ConstructionService):
        self.service = service
