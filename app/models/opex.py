from decimal import Decimal

from sqlalchemy import ForeignKey, Integer, Numeric
from sqlalchemy.orm import Mapped, mapped_column

from app.core.database import Base


class OpexByBedrooms(Base):
    __tablename__ = "opex_by_bedrooms"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    market: Mapped[int | None] = mapped_column(Integer, ForeignKey("market_keys_master.id"))
    bedrooms: Mapped[int | None] = mapped_column(Integer)
    pool_hot_tub_low: Mapped[Decimal | None] = mapped_column(Numeric)
    pool_hot_tub_high: Mapped[Decimal | None] = mapped_column(Numeric)
    outdoor_landscaping: Mapped[Decimal | None] = mapped_column(Numeric)
    software: Mapped[Decimal | None] = mapped_column(Numeric)
    insurance_hoi: Mapped[Decimal | None] = mapped_column(Numeric)
    supplies: Mapped[Decimal | None] = mapped_column(Numeric)
    capex_reserve: Mapped[Decimal | None] = mapped_column(Numeric)
    cleaning_fee: Mapped[Decimal | None] = mapped_column(Numeric)
    num_of_turns: Mapped[int | None] = mapped_column(Integer)
    property_taxes: Mapped[Decimal | None] = mapped_column(Numeric)
    land_value: Mapped[Decimal | None] = mapped_column(Numeric)
    appreciation: Mapped[Decimal | None] = mapped_column(Numeric)
    hoa_fees: Mapped[Decimal | None] = mapped_column(Numeric)
    furnishings_low: Mapped[Decimal | None] = mapped_column(Numeric)
    furnishings_high: Mapped[Decimal | None] = mapped_column(Numeric)
    consolidated_shipping: Mapped[Decimal | None] = mapped_column(Numeric)


class OpexBySize(Base):
    __tablename__ = "opex_by_size"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    market: Mapped[int | None] = mapped_column(Integer, ForeignKey("market_keys_master.id"))
    sqft: Mapped[int | None] = mapped_column(Integer)
    internet: Mapped[Decimal | None] = mapped_column(Numeric)
    pest_control: Mapped[Decimal | None] = mapped_column(Numeric)
    utilities: Mapped[Decimal | None] = mapped_column(Numeric)
