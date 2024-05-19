from xarizmi.candlestick import Candlestick


class TestCandlestick:

    def test(self):
        c = Candlestick()
        assert isinstance(c, Candlestick)
