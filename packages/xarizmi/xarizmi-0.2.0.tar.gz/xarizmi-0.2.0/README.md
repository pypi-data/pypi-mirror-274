# Xarizmi
Xarizmi (read Khwarizmi) project is an educational project that contains tools for technical analysis in Python.


## Installation
```bash
pip install xarizmi
```

## Example

### Build Candlestick
```python
from xarizmi.candlestick import Candlestick
c = Candlestick(
    **{
        "open": 2,
        "low": 1,
        "high": 4,
        "close": 3,
    }
)
```


