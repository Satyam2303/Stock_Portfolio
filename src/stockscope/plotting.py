from __future__ import annotations

from typing import Optional

import pandas as pd
import matplotlib.pyplot as plt

from .exceptions import InvalidInputError
from .indicators import sma
from .risk import max_drawdown


def plot_price(series: pd.Series, title: str = "Price", show: bool = True):
    if not isinstance(series, pd.Series) or series.empty:
        raise InvalidInputError("series must be a non-empty pandas Series.")
    fig, ax = plt.subplots()
    ax.plot(series.index, series.values)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Price")
    ax.grid(True)
    if show:
        plt.show()
    return fig, ax


def plot_price_with_sma(series: pd.Series, window: int = 20, title: Optional[str] = None, show: bool = True):
    if not isinstance(series, pd.Series) or series.empty:
        raise InvalidInputError("series must be a non-empty pandas Series.")
    ma = sma(series, window=window)
    fig, ax = plt.subplots()
    ax.plot(series.index, series.values, label="Price")
    ax.plot(ma.index, ma.values, label=f"SMA({window})")
    ax.set_title(title or f"Price + SMA({window})")
    ax.set_xlabel("Date")
    ax.set_ylabel("Value")
    ax.grid(True)
    ax.legend()
    if show:
        plt.show()
    return fig, ax


def plot_drawdown(series: pd.Series, title: str = "Drawdown", show: bool = True):
    if not isinstance(series, pd.Series) or series.empty:
        raise InvalidInputError("series must be a non-empty pandas Series.")
    dd = max_drawdown(series)
    fig, ax = plt.subplots()
    ax.plot(dd.index, dd.values)
    ax.set_title(title)
    ax.set_xlabel("Date")
    ax.set_ylabel("Drawdown")
    ax.grid(True)
    if show:
        plt.show()
    return fig, ax
