from pydantic import BaseModel, model_validator


class UnderwritingQuerySchema(BaseModel):
    bedrooms: int
    sqft: int
    market_id: int | None = None
    market_slug: str | None = None

    @model_validator(mode="after")
    def market_slug_takes_precedence(self):
        if self.market_id is not None and self.market_slug is not None:
            self.market_id = None
        return self
