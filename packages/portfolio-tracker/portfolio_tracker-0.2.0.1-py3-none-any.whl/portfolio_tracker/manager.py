"""
This module that contains the portfolio class and the functions to manage it.
"""
import os
from typing import Literal, Optional, Tuple, Callable

import numpy as np
import pandas as pd

from .price_repo import PriceRepo
from .utils import roll_day_to_bday, compute_rtn, compute_cum_rtn, string_period_to_bdays


def load_raw_stock_df(stock_df_path: str | os.PathLike) -> Tuple[pd.Series, pd.DataFrame, pd.Timestamp]:
    """
    Function that load the raw stock DataFrame and returns the weights, the stock info DataFrame and the date.

    Notes:
        - if anyone want to change the input Excel file, it must change this function accordingly.
        - Weights: is a Series with the stocks as index, and the weights as values.
        - Stock info: is a DataFrame with the stocks as index, and the columns containing any other information
            contained in the excel (every column must be lowercase and with '_' instead of spaces).
        - Date: Date of allocation (in pd.Timestamp format), it must be a day when the markets are open.
    """
    stock_df = pd.read_excel(stock_df_path)
    stock_df.columns = stock_df.columns.str.lower().str.replace(' ', '_')
    stock_df = stock_df.set_index('ticker')

    weights = stock_df['weights']
    date = stock_df['start_date'].mode()[0]
    stock_df = stock_df.drop(columns=['weights', 'start_date'])

    if isinstance(stock_df, pd.Series):
        stock_df = stock_df.to_frame(name=stock_df.name)
    if isinstance(date, str):
        date = pd.Timestamp(date)

    # We take the closest trading day (can be the same)
    date = roll_day_to_bday(date, offset=0)
    return weights, stock_df, date


class Portfolio:
    """
    Class that manages the portfolio, which is made of

    - Weights [index=date, columns=stocks]: DataFrame that contains the weights at each date.
    - Returns [index=date, columns=stocks]: DataFrame that contains the log returns of each asset at each date.
    - History log [index=date, columns=stocks]: DataFrame that contains the weights before and after each rebalancing date.
    - Stocks info [index=stocks, columns=info]: DataFrame that contains the information of each asset.

    Weights dataframe is not normalized, cause it represents the value gained (or lost) by each asset
    (which makes easier to carry out the rebalancing)

    The Portfolio class is designed to work with the load_raw_stock_df function, which takes an Excel file
    (with arbitrary formatting) and returns:

    - Weights: Series with the stocks as index, and the weights as values (each row must sum to 1).
    - Stock info: DataFrame with the stocks as index, and some columns containing any other information.
    - Date: Date of allocation (in pd.Timestamp format), it must be a day when the markets are open.

    The Portfolio class has the following functionalities:

    - Constructor: Initialize the Portfolio with some stocks and weights.
    - Roll forward: Roll the portfolio forward for a given offset by using the last weights.
    - Rebalancing: Rebalance the portfolio with the new weights at a given date.

    The portfolio, at each rebalance will update its internal dataframe, to add new stocks with their weights or to
    update the weights of the existing ones, then it will update the log and compute the new returns
    (based on those weights).

    For the portfolio to be able to read xlsx uses a function named load_fn (by default load_raw_stock_df),
    which takes the path of the xlsx file and returns the weights, the stock info DataFrame, and the date;
    it can be overridden to load the data in a different format (check the load_raw_stock_df function for more info).

    It's recommended to use the Portfolio class with the PriceRepo class, to have an efficient way to get the prices;
    also, is advocate to extract information from a Portfolio with the get methods, that provides some useful features
    (such as normalization, weighted returns, etc.).
    """

    def __init__(self, stock_df_path: str | os.PathLike, prices_repo_close: PriceRepo, price_repo_open: PriceRepo,
                 load_fn: Optional[Callable[[str | os.PathLike], Tuple[pd.Series, pd.DataFrame, pd.Timestamp]]]
                 = load_raw_stock_df):
        """
        Function that initializes the Portfolio object by loading the stock DataFrame and the price repositories.
        Note: prices_repo_close should take the closing price (Close or Adj Close)
        and prices_repo_open the opening price (Open).
        """
        self._load_fn = load_fn
        self.prices_repo = prices_repo_close  # the default price repo is the close one
        self.prices_repo_open = price_repo_open

        w, stocks_info, date = self._load_fn(stock_df_path)
        self._weights = w.to_frame(name=date).transpose()
        self._returns = pd.DataFrame(index=[date], columns=stocks_info.index, data=0)
        self._history_log = self._create_history_log(date, pd.Series(index=stocks_info.index, data=0), w)
        self._stocks_info = stocks_info

    @staticmethod
    def _init_date(date: str | pd.Timestamp) -> pd.Timestamp:
        if isinstance(date, str):
            date = pd.Timestamp(date)
        return date

    @staticmethod
    def _create_history_log(date: str | pd.Timestamp, weights_bef: pd.Series, weights_aft: pd.Series | None = None):
        """Function for the creation of the history log with a single row
        (representing the weights before and after a date)."""
        if isinstance(date, str):
            date = pd.Timestamp(date)

        multi_index = pd.MultiIndex.from_product([weights_bef.index, ['before', 'after']],
                                                 names=['stock', 'weights'])
        history_log = pd.DataFrame(index=[date], columns=multi_index)
        history_log.loc[date, (weights_bef.index, 'before')] = weights_bef.values
        if weights_aft is not None:
            history_log.loc[date, (weights_aft.index, 'after')] = weights_aft.values
        return history_log

    def _get_property_in_dates(self, dates: Tuple[str | pd.Timestamp, Optional[str | pd.Timestamp]] | None,
                               property: pd.DataFrame) -> pd.DataFrame:
        if dates is not None:
            start_date = self._init_date(dates[0])
            end_date = self._init_date(dates[1]) if dates[1] is not None else property.index[-1]
            return property.loc[start_date:end_date].dropna(how='all')
        return property

    def get_weights(self, dates: Optional[Tuple[str | pd.Timestamp, Optional[str | pd.Timestamp]]] = None):
        """
        Function that returns the normalized weights of the assets in the portfolio between two dates
        (or in the entire history).
        """
        weights = self._get_property_in_dates(dates, self._weights)
        return weights.div(weights.sum(axis=1), axis=0)

    def get_assets_values(self, dates: Optional[Tuple[str | pd.Timestamp, Optional[str | pd.Timestamp]]] = None):
        """
        Function that returns the values of the assets in the portfolio between two dates (or in the entire history).

        The values are the weights not normalized, so they represent the value gained (or lost) by each asset.
        """
        return self._get_property_in_dates(dates, self._weights)

    def get_returns(self, dates: Optional[Tuple[str | pd.Timestamp, Optional[str | pd.Timestamp]]] = None,
                    weighted: bool = True):
        """Function that returns the returns of the portfolio between two dates (or in the entire history)."""
        rtns = self._get_property_in_dates(dates, self._returns)
        if not weighted:
            return rtns
        weights = self.get_weights(dates)
        return weights * rtns

    def get_history_log(self, dates: Optional[Tuple[str | pd.Timestamp, Optional[str | pd.Timestamp]]] = None,
                        normalize: bool = True) -> pd.DataFrame:
        """Function that returns the history log of the portfolio between two dates (or in the entire history)."""
        h_log = self._get_property_in_dates(dates, self._history_log)

        if not normalize:
            return h_log

        before_total = h_log.loc[:, (slice(None), "before")].sum(axis=1)
        after_total = h_log.loc[:, (slice(None), "after")].sum(axis=1)

        h_log.loc[:, (slice(None), "before")] = h_log.loc[:, (slice(None), "before")].div(before_total, axis=0)
        h_log.loc[:, (slice(None), "after")] = h_log.loc[:, (slice(None), "after")].div(after_total, axis=0)

        return h_log.astype(float).fillna(0)

    @property
    def returns(self):
        return self.get_returns()

    @property
    def history_log(self) -> pd.DataFrame:
        return self._history_log

    @property
    def weights(self):
        return self.get_weights()

    @property
    def assets_values(self):
        return self.get_assets_values()

    @property
    def stocks_info(self) -> pd.DataFrame:
        return self._stocks_info

    def roll_forward(self, offset: str | int | Literal["M", "3M", "1Y", "5Y"] | pd.Timestamp):
        """
        Function that roll the portfolio forward for a given offset by using the current weights

        Offset can be:

        - A string representing the offset ('M', '3M', '1Y', '5Y'),
        - An integer representing the number of bdays.
        - A date in format 'YYYY-MM-DD' or pd.Timestamp.
        """
        if offset in ["M", "3M", "1Y", "5Y"]:
            offset = string_period_to_bdays(str(offset))
        if isinstance(offset, int):
            end_date = roll_day_to_bday(self._weights.index[-1], offset=offset)

        elif isinstance(offset, pd.Timestamp) or isinstance(offset, str):
            if isinstance(offset, str):
                offset = pd.Timestamp(offset)
            if offset <= self._weights.index[-1]:
                raise ValueError("The date must be after the last date in the portfolio.")
            end_date = offset
        else:
            raise ValueError("Invalid offset type.")

        weights = self._weights.iloc[-1]
        start_date = self._weights.index[-1]  # We take one day before for the rtn

        prices = self.prices_repo.get_prices(weights.index.values.tolist(), start_date, end_date)
        rtns = compute_rtn(prices)
        rtns_cum = compute_cum_rtn(rtns)
        rolled_weights = np.exp(rtns_cum) * weights
        rtns.loc[:, weights == 0] = 0  # We take only the returns of the stocks with weight > 0

        self._weights = pd.concat([self._weights, rolled_weights])
        self._returns = pd.concat([self._returns, rtns])

    def roll_backward(self, offset: str | int | Literal["M", "3M", "1Y", "5Y"] | pd.Timestamp):
        """Function used to delete data from the portfolio by rolling backward for a given offset."""
        if offset in ["M", "3M", "1Y", "5Y"]:
            offset = string_period_to_bdays(str(offset))
        if isinstance(offset, int):
            date = roll_day_to_bday(self._weights.index[-1], offset=offset, direction='backward')
        elif isinstance(offset, str) or isinstance(offset, pd.Timestamp):
            if isinstance(offset, str):
                offset = pd.Timestamp(offset)
            date = offset
        else:
            raise ValueError("Invalid offset type.")

        self._weights = self._weights.loc[:date].iloc[:-1]  # we go back to date-1
        self._returns = self._returns.loc[:date].iloc[:-1]
        if date in self._history_log.index:
            self._history_log = self._history_log.loc[:date].iloc[:-1]

    def _rebalance_weights(self, target_weights: pd.Series, common_stocks, date):
        # We unify the indexes to apply operations on them
        target_weights = target_weights.reindex(common_stocks, fill_value=0)

        new_weights = target_weights * self._weights.iloc[-1].sum()
        new_weights_df = new_weights.to_frame(name=date).transpose()

        # We insert the new stocks in the weights DataFrame
        weights_reindex = self._weights.transpose().reindex(common_stocks, fill_value=0).transpose()

        new_history_log = self._create_history_log(date, weights_reindex.iloc[-1], new_weights)
        history_log_reindex = self._history_log.transpose().reindex(new_history_log.columns, fill_value=0).transpose()

        # we add the new weights and the new history log to the old ones
        return pd.concat([weights_reindex, new_weights_df]), pd.concat([history_log_reindex, new_history_log])

    def _rebalance_returns(self, common_stocks, date):
        # We reindex the returns DataFrame
        returns_reindex = self._returns.transpose().reindex(common_stocks, fill_value=0).transpose()

        opening_price = self.prices_repo_open.get_prices(common_stocks.values.tolist(), date,
                                                         roll_day_to_bday(date, offset=1))
        opening_price = opening_price.iloc[0].to_frame().transpose()

        closing_price = self.prices_repo.get_prices(common_stocks, date, roll_day_to_bday(date, offset=1))
        closing_price = closing_price.iloc[0].to_frame().transpose()
        new_returns = compute_rtn(pd.concat([opening_price, closing_price]))

        return pd.concat([returns_reindex, new_returns])

    def rebalancing(self, target_weights: pd.Series, new_stock_info: Optional[pd.DataFrame] = None,
                    date: Optional[str | pd.Timestamp] = None, auto_roll: bool = True,
                    force_rebalancing: bool = False):
        """
        Function that rebalances the portfolio with the new weights at a given date (or on the last one);
        it also uses the new_stock_info to add new information, or new stocks to the stocks_info DataFrame.

        Notes:
            - With auto_roll=True, the function will roll the portfolio forward to the rebalance date if needed
            - With force_rebalancing=True, the function will rebalance the portfolio even if the date is already
            present by overwriting the weights and the returns.
        """
        if date is None:
            date = self._weights.index[-1]
        else:
            if isinstance(date, str):
                date = pd.Timestamp(date)

        if date in self._weights.index:
            if not force_rebalancing:
                raise ValueError("The date is already present in the portfolio,"
                                 " use force_rebalancing=True to overwrite.")
            else:
                self.roll_backward(date)

        else:
            if date < self._weights.index[0]:
                raise ValueError("The date must be after the first date in the portfolio.")
            elif date > roll_day_to_bday(self._weights.index[-1], offset=1):
                # if there is a gap between the last date and the new one, we roll forward till the new date-1
                if auto_roll:
                    self.roll_forward(roll_day_to_bday(date, offset=1, direction='backward'))
                else:
                    raise ValueError("The date must be before the next trading day, use auto_roll=True to roll forward"
                                     " to the rebalance date.")

        common_stocks = self._weights.columns.union(target_weights.index)

        if new_stock_info is not None:
            for col in (col for col in new_stock_info.columns if col not in self._stocks_info.columns):
                self._stocks_info[col] = np.NAN  # Initialize possible new columns with NaN

            # We add the new stocks to the DataFrame
            self._stocks_info = self._stocks_info.reindex(common_stocks, fill_value=np.NAN)
            self._stocks_info.update(new_stock_info)  # We update the stocks info DataFrame

        self._weights, self._history_log = self._rebalance_weights(target_weights, common_stocks, date)
        self._returns = self._rebalance_returns(common_stocks, date)

    def rebalancing_from_file(self, stock_df_path: str | os.PathLike, force_rebalancing: bool = False,
                              auto_roll: bool = True):
        """
        Function that rebalances the portfolio with the new weights from a file, it also uses the new_stock_info to add
        new information, or new stocks to the stocks_info DataFrame.

        Note: with force_rebalancing=True, the function will rebalance the portfolio even if the date is already
        present by overwriting the weights and the returns.
        """
        w, stocks_info, date = self._load_fn(stock_df_path)
        self.rebalancing(w, stocks_info, date, force_rebalancing=force_rebalancing, auto_roll=auto_roll)

    def get_rebalance_operation(self, date: Optional[str | pd.Timestamp] = None, normalize: bool = True) -> pd.Series:
        """Function that returns the operation of the rebalance at a given date, which is a Series that for each stock
        contains how much we have to buy or sell to reach the target weights."""
        if date is None:
            date = self._history_log.index[-1]
        else:
            if isinstance(date, str):
                date = pd.Timestamp(date)

        if date not in self._weights.index:
            raise ValueError("The date is not present in the portfolio.")

        rebalance_log = self.get_history_log((date, date), normalize=normalize).iloc[0]
        return rebalance_log[slice(None), "after"] - rebalance_log[slice(None), "before"]
