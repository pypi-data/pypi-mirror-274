from pydantic import BaseModel
from pydantic import NonNegativeFloat


class Candlestick(BaseModel):
    close: NonNegativeFloat
    open: NonNegativeFloat
    low: NonNegativeFloat
    high: NonNegativeFloat


class CandlestickChart(BaseModel):
    candles: list[Candlestick]
