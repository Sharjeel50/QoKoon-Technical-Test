from datetime import date, timedelta
from typing import Optional, Annotated

from fastapi import APIRouter, Depends, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session
from starlette.responses import JSONResponse

import pandas as pd

from .constants import TimeFrameEnum, TIME_FRAME_DICT
from .models import Pnl, WorkingCapital
from .service import calculate_cash_flow
from src.database import get_db

router = APIRouter(prefix='/cash-flow')


# Future todo - Add in more timeframes, e.g. 2, 5, 10 year periods to test and verify application performace.

@router.get("/calculate",
            summary="Calculate cash flow based on start date and time frame",
            description="Calculate Cash Flow: A method to calculate cash flow from operations. This method "
                        "adjusts the Net Income for non-cash charges (Depreciation) and changes in working "
                        "capital components (Inventory, Accounts Receivable, Accounts Payable).",
            responses={
                status.HTTP_200_OK: {
                    "description": "Successful Response",
                    "content": {
                        "application/json": {
                            "example": {
                                "data": {
                                    "non_cash_charges": 1.0,
                                    "changes_in_working_capital": 1.0,
                                    "cash_flow_from_operations": 1.0,
                                }
                            }
                        }
                    }
                },
                status.HTTP_400_BAD_REQUEST: {"description": "Bad Request"},
            })
def get_cash_flow(start_date: date,
                  timeframe: TimeFrameEnum,
                  include_working_data: Annotated[Optional[bool], "Include working data in response"] = None,
                  session: Session = Depends(get_db)) -> JSONResponse:
    """
    Endpoint to calculate cash flow according to start date and time frame.

    :param start_date: The start date for the cash flow calculation.
    :param timeframe: The time frame for the cash flow calculation (monthly, quarterly, yearly).
    :param include_working_data: Include working data in the response (optional).
    :param session: Database session.
    :return: JSON response with calculated cash flow data.
    """

    timeframe_date = start_date + timedelta(days=TIME_FRAME_DICT[timeframe])

    pnl_query = session.query(Pnl).filter(Pnl.date >= start_date, Pnl.date <= timeframe_date)
    working_capital_query = session.query(WorkingCapital).filter(WorkingCapital.date >= start_date,
                                                                 WorkingCapital.date <= timeframe_date)
    # Convert data to DataFrames for easier processing
    pnl_dataframe = pd.read_sql(pnl_query.statement, session.bind)
    working_capital_dataframe = pd.read_sql(working_capital_query.statement, session.bind)

    cash_flow_values = {
        "msg": "No data present for start date and time frame provided",
        "data": None
    }

    if not pnl_dataframe.empty:
        cash_flow_values = calculate_cash_flow(pnl_dataframe, working_capital_dataframe, include_working_data)

    return JSONResponse(content={"data": jsonable_encoder(cash_flow_values)})
