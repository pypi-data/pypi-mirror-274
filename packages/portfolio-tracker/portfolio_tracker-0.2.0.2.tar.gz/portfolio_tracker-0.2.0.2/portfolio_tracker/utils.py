"""
This module includes utility functions that are used in the project.
"""
import pandas as pd
from typing import List, Literal, Optional, Tuple
import numpy as np
import pandas_market_calendars as mcal

DEF_CALENDAR = 'NYSE'


def get_trading_days(start: str | pd.Timestamp, end: str | pd.Timestamp,
                     calendar: str = DEF_CALENDAR) -> List[pd.Timestamp]:
    """ Function that returns the trading days between two dates. """
    if isinstance(start, str):
        start = pd.Timestamp(start)
    if isinstance(end, str):
        end = pd.Timestamp(end)

    nyse = mcal.get_calendar(calendar)
    return nyse.valid_days(start_date=start, end_date=end, tz=None)


def roll_day_to_bday(date: pd.Timestamp | str, offset: int = 0,
                     direction: Literal["forward", "backward", "f", "b"] = "forward",
                     calendar: str = DEF_CALENDAR) -> pd.Timestamp:
    """
    Function that roll a date to the next or previous business day, given an offset and a direction.
    With offset=0, the function returns the nearest business day to the input date.
    """
    if isinstance(date, str):
        date = pd.Timestamp(date)
    if offset < 0:
        raise ValueError("Offset must be a positive integer or zero (for negative offset use the direction parameter)")

    bday_offset = offset + 2 * int(offset / 5) + int(20 * offset / 252) + 5  # Adjust for weekends and holidays

    if direction in ["forward", "f"]:
        return get_trading_days(date, date + pd.Timedelta(days=bday_offset), calendar=calendar)[offset]

    else:
        return get_trading_days(date + pd.Timedelta(days=-bday_offset), date, calendar=calendar)[-(offset + 1)]


def compute_rtn(prices_df: pd.DataFrame) -> pd.DataFrame:
    """
    Compute the daily log returns from the prices DataFrame.
    """
    daily_returns = np.log(prices_df / prices_df.shift(1)).dropna(how='all')
    if isinstance(daily_returns, pd.Series):
        daily_returns = daily_returns.to_frame(name=daily_returns.name)

    return daily_returns.dropna(how='all')


def compute_cum_rtn(returns_df: pd.DataFrame,
                    period: Optional[Tuple[str, Optional[str]] | Literal["M", "3M", "1Y", "5Y", "YTD"] | int] = None
                    ) -> pd.DataFrame:
    """
    Function that computes the cumulative returns for a given period, which correspond to the max lookback date
    (except for the tuple case).

    Period can be:
    - A tuple of two explict dates (start, end) in the format 'YYYY-MM-DD',
    - A string representing the period ('3M', '1Y', '5Y', 'YTD'),
    - An integer representing the number of bdays.
    - None, which means the entire DataFrame.
    """
    if period is None:
        returns_data = returns_df
    elif isinstance(period, tuple):
        start, end = period

        if end is None:  # If end is None, we take the last date in the DataFrame
            end = returns_df.index[-1]
        else:
            end = pd.Timestamp(end)
        start = pd.Timestamp(start)

        if start >= end or start not in returns_df.index or end not in returns_df.index:
            raise ValueError("Invalid dates.")
        returns_data = returns_df.loc[start:end]

    elif isinstance(period, str):
        if period == "YTD":
            returns_data = returns_df.loc[returns_df.index.year == returns_df.index[-1].year]
        else:
            returns_data = returns_df.loc[-string_period_to_bdays(period):]
    elif isinstance(period, int):
        returns_data = returns_df[-period:]
    else:
        raise ValueError("Invalid period type.")

    cum_returns = returns_data.cumsum()
    return cum_returns


def string_period_to_bdays(period: str) -> int | None:
    """Function that convert a string period to the number of bdays."""
    match period:
        case "M" | "1M":
            return 21
        case "3M":
            return 63
        case "1Y":
            return 252
        case "5Y":
            return 1260
        case _:
            return None
