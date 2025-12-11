from __future__ import annotations

from typing import Union

import numpy as np
import pandas as pd

from .exceptions import InvalidInputError


SeriesOrFrame = Union[pd.Series, pd.DataFrame]


def _ensure_series_or_frame(x: SeriesOrFrame, name: str) -> SeriesOrFrame:
    if not isinstance(x, (pd.Series, pd.DataFrame)):
        raise InvalidInputError(f"{name} must be a pandas Series or DataFrame.")
    if x.empty:
        raise InvalidInputError(f"{name} cannot be empty.")
    return x


def daily_returns(prices: SeriesOrFrame) -> SeriesOrFrame:
    prices = _ensure_series_or_frame(prices, "prices")
    rets = prices.pct_change()
    return rets.dropna(how="all")


def log_returns(prices: SeriesOrFrame) -> SeriesOrFrame:
    prices = _ensure_series_or_frame(prices, "prices")
    rets = np.log(prices / prices.shift(1))
    return rets.dropna(how="all")


def sma(series: SeriesOrFrame, window: int) -> SeriesOrFrame:
    series = _ensure_series_or_frame(series, "series")
    if not isinstance(window, int) or window <= 0:
        raise InvalidInputError("window must be a positive integer.")
    return series.rolling(window=window).mean()


def ema(series: SeriesOrFrame, span: int) -> SeriesOrFrame:
    series = _ensure_series_or_frame(series, "series")
    if not isinstance(span, int) or span <= 0:
        raise InvalidInputError("span must be a positive integer.")
    return series.ewm(span=span, adjust=False).mean()


def rsi(series: pd.Series, window: int = 14) -> pd.Series:
    if not isinstance(series, pd.Series):
        raise InvalidInputError("RSI input must be a pandas Series (single ticker series).")
    if series.empty:
        raise InvalidInputError("series cannot be empty.")
    if not isinstance(window, int) or window <= 0:
        raise InvalidInputError("window must be a positive integer.")

    delta = series.diff()
    gain = delta.clip(lower=0.0)
    loss = -delta.clip(upper=0.0)

    avg_gain = gain.rolling(window=window).mean()
    avg_loss = loss.rolling(window=window).mean()

    rs = avg_gain / avg_loss.replace(0, np.nan)
    rsi_val = 100 - (100 / (1 + rs))
    return rsi_val
