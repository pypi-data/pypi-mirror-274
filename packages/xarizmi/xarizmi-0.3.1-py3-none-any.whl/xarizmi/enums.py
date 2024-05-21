from enum import IntEnum
from enum import StrEnum


class TimeUnitsSeconds(IntEnum):
    MIN = 60
    HOUR = 60 * 60
    DAY = 60 * 60 * 24
    WEEK = 60 * 60 * 24 * 7
    MONTH = 60 * 60 * 24 * 7 * 30


class SideEnum(StrEnum):
    BUY = "BUY"
    SELL = "SELL"


class IntervalTypeEnum(StrEnum):
    MIN_1 = "1min"
    MIN_3 = "3min"
    MIN_5 = "5min"
    MIN_15 = "15min"
    MIN_30 = "30min"
    HOUR_1 = "1hour"
    HOUR_2 = "2hour"
    HOUR_4 = "4hour"
    HOUR_6 = "6hour"
    HOUR_8 = "8hour"
    HOUR_12 = "12hour"
    DAY_1 = "1day"
    WEEK_1 = "1week"
    MONTH_1 = "1month"

    @staticmethod
    def get_interval_in_seconds(
        interval_type: "IntervalTypeEnum",
    ) -> None | int:
        unit: str | None = None
        value: int | None = None
        for prefix in [
            "MIN_",
            "HOUR_",
            "DAY_",
            "WEEK_",
            "MONTH_",
        ]:
            if interval_type.name.startswith(prefix):
                unit = prefix.replace("_", "")
                value = int(interval_type.split(prefix)[-1])
                break
        if unit is not None and value is not None:
            return value * TimeUnitsSeconds[unit].value
        else:
            raise NotImplementedError(
                f"Not implemented for interval_type = '{interval_type}'"
            )
