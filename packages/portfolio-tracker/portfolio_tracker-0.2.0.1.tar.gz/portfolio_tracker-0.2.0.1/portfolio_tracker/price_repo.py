"""
This module manages the stock prices repository, which is a csv file containing the prices of the stocks, that will be
used during multiple executions of the program to avoid downloading the prices every time.
"""
import os
from typing import List, Optional, Literal

import pandas as pd
import yfinance as yf

from .utils import get_trading_days, roll_day_to_bday


class PriceRepo:
    """
    Class that manages the stock prices repository, which is a DataFrame/csv file containing the prices of the stocks,
    that will be used during multiple executions of the program to avoid downloading the prices every time.
    """

    def __init__(self, path: str | os.PathLike,
                 price_type: Literal['Open', 'High', 'Low', 'Close', 'Adj Close', 'Volume'] = 'Adj Close'):
        self.path = path
        if not os.path.exists(path):  # Create a dummy repo if it does not exist
            dummy_stock_prices = pd.DataFrame(index=pd.date_range(pd.Timestamp.today().date() - pd.DateOffset(days=1),
                                                                  pd.Timestamp.today().date(), freq='D', name='date'))
            dummy_stock_prices.to_csv(path)
        self.price_type = price_type
        self._price_df = pd.read_csv(path, index_col='date', parse_dates=True)

    @property
    def price_df(self) -> pd.DataFrame:
        return self._price_df

    def _download_stocks_prices(self, tickers_list: List[str], start: pd.Timestamp, end: pd.Timestamp) -> pd.DataFrame:
        """
        Download daily prices from yfinance from a list of tickers, within a specified date range.
        """
        prices_df = yf.download(tickers_list, start=start, end=end)[self.price_type]
        if isinstance(prices_df, pd.Series):  # If only one stock is downloaded, we convert the series to a DataFrame
            prices_df = prices_df.to_frame(name=tickers_list[0])
        return prices_df

    def _stock_in_repo(self, ticker: str, start: pd.Timestamp, end: pd.Timestamp) -> bool:
        """
        Check if the stock prices are already in the repo or if there are missing date (in the selected range) in the repo.
        """
        if ticker not in self._price_df.columns:
            return False
        if self._price_df.loc[start:end, ticker].isna().any():
            return False
        return True

    def get_prices(self, tickers_list: List[str], start: str | pd.Timestamp, end: Optional[str | pd.Timestamp] = None,
                   ) -> pd.DataFrame:
        """Function that return the df prices of a list of tickers, by loading them from the repo or by
        downloading them from yfinance if a stock prices is not available, then it returns the selected stocks
        and the update price_repo.

        Notes: The start and end must be in the format 'YYYY-MM-DD'. (if end is None,it will download until 2 weeks ago)
        """
        # Convert the dates to trading dates
        if end is None:
            end = (pd.Timestamp.today() - pd.Timedelta(days=13)).strftime('%Y-%m-%d')
        else:
            end = roll_day_to_bday(end, offset=1).strftime('%Y-%m-%d')  # Add one day to include the end date

        trading_period = pd.Index(get_trading_days(start, end))
        start, end, end_aft = trading_period[0], trading_period[-2], trading_period[-1]  # end_aft is one bday after
        trading_period = trading_period[:-1]  # Remove the extra day to avoid including it in the repo

        if start > end:
            raise ValueError("The start date must be before the end date.")

        if not trading_period.isin(self._price_df.index).all():  # if the period is not in the repo, reindex the repo
            index_name = self._price_df.index.name
            self._price_df = self._price_df.reindex(self._price_df.index.union(trading_period))
            self._price_df.index.name = index_name

        # Check which stocks need to be downloaded
        tickers_to_download = [ticker for ticker in tickers_list if not self._stock_in_repo(ticker, start, end)]

        if len(tickers_to_download) > 0:  # If all the stocks are already in the repo, return the prices selected
            new_prices = self._download_stocks_prices(tickers_to_download, start,
                                                      end_aft)  # end_aft to include the last day
            self._price_df.loc[start:end, tickers_to_download] = new_prices  # Update the repo with the new prices

            self._price_df.to_csv(self.path)  # Save the updated repo

        return self._price_df.loc[start:end, tickers_list]
