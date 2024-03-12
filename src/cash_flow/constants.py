from enum import Enum


class TimeFrameEnum(str, Enum):
    MONTHLY = "monthly"
    QUARTERLY = "quarterly"
    YEARLY = "yearly"


TIME_FRAME_DICT = {
    TimeFrameEnum.MONTHLY.value: 30,
    TimeFrameEnum.QUARTERLY.value: 90,
    TimeFrameEnum.YEARLY.value: 365
}
