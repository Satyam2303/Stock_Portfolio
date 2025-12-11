from __future__ import annotations

from typing import Union

import numpy as np
import pandas as pd

from .exceptions import InvalidInputError


SeriesOrFrame = Union[pd.Series, pd.DataFrame]


def volatility(returns: SeriesOrFrame, annualize: bool = True, periods_per_year: int = 252) -> SeriesOrFrame:
    if not isinstance(returns, (pd.Series, pd.DataFrame)):
        raise InvalidInputError("returns must be a pandas Series or DataFrame.")
    if returns.empty:
        raise InvalidInputError("returns cannot be empty.")
    if not isinstance(periods_per_year, int) or periods_per_year <= 0:
        raise InvalidInputError("periods_per_year must be a positive integer.")

    vol = returns.std(ddof=1)
    if annualize:
        vol = vol * np.sqrt(periods_per_year)
    return vol


def max_drawdown(prices: pd.Series) -> pd.Series:
    if not isinstance(prices, pd.Series):
        raise InvalidInputError("prices must be a pandas Series (single ticker).")
    if prices.empty:
        raise InvalidInputError("prices cannot be empty.")

    running_max = prices.cummax()
    drawdown = prices / running_max - 1.0
    return drawdown


def value_at_risk(returns: pd.Series, level: float = 0.05) -> float:
    if not isinstance(returns, pd.Series):
        raise InvalidInputError("returns must be a pandas Series (single ticker or portfolio).")
    if returns.empty:
        raise InvalidInputError("returns cannot be empty.")
    try:
        level = float(level)
    except Exception:
        raise InvalidInputError("level must be a float like 0.05.")
    if not (0 < level < 1):
        raise InvalidInputError("level must be between 0 and 1 (e.g., 0.05).")

    clean = returns.dropna()
    if clean.empty:
        raise InvalidInputError("returns contain only NaNs.")
    # Historical VaR: percentile of returns distribution
    return float(clean.quantile(level))
