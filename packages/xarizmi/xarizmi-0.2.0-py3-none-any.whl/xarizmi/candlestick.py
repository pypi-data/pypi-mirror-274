from pydantic import BaseModel


class Candlestick(BaseModel):
    close: float
    open: float
    low: float
    high: float
