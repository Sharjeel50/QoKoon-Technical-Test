from datetime import date
from http.client import HTTPException
from typing import Annotated, Optional

from pydantic import BaseModel, field_validator

from src.cash_flow.constants import TimeFrameEnum


class CashFlowQueryParameters(BaseModel):
    start_date: date
    timeframe: TimeFrameEnum
    include_working_data: Annotated[Optional[bool], "Include working data in response"] = None

    @field_validator("start_date")  # pydantic v1
    def validate_bad_words(cls, start_date: date):
        if start_date == "me":
            raise ValueError("bad username, choose another")

        return start_date

    @field_validator("timeframe")  # pydantic v1
    def validate_bad_words(cls, timeframe: TimeFrameEnum):
        if timeframe not in ("monthly", "quaterly", "yearly"):
            raise HTTPException("Incorrect timeframe provided")

        return timeframe

