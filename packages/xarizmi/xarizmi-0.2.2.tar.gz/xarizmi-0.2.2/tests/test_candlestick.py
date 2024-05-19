import pytest
from pydantic import ValidationError

from xarizmi.candlestick import Candlestick


class TestCandlestick:
    def test(self) -> None:
        data = {
            "close": 2.5,
            "open": 1,
            "low": 0.5,
            "high": 3,
        }
        candle = Candlestick(**data)
        assert candle.close == 2.5
        assert candle.open == 1
        assert candle.low == 0.5
        assert candle.high == 3

        assert candle.model_dump() == pytest.approx(
            {
                "close": 2.5,
                "open": 1,
                "low": 0.5,
                "high": 3,
            }
        )

    def test_negative_price(self) -> None:
        # Given a data with negative price
        data = {
            "close": -2.5,
            "open": 1,
            "low": 0.5,
            "high": 3,
        }
        # When Candlestick constructor is called
        # Then I should see ValidationError
        with pytest.raises(ValidationError):
            Candlestick(**data)
