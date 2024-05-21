from pydantic import BaseModel
from pydantic import NonNegativeFloat

from xarizmi.enums import IntervalTypeEnum


class Candlestick(BaseModel):
    close: NonNegativeFloat
    open: NonNegativeFloat
    low: NonNegativeFloat
    high: NonNegativeFloat
    interval_type: IntervalTypeEnum | None = None
    interval: int | None = None  # interval in seconds


class CandlestickChart(BaseModel):
    candles: list[Candlestick]
