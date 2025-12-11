from __future__ import annotations

from typing import Union, Iterable, Optional

import pandas as pd
import yfinance as yf

from .exceptions import InvalidInputError, DataDownloadError, EmptyDataError
from .utils import ensure_ticker_list, parse_date, validate_date_range


_ALLOWED_INTERVALS = {"1d", "5d", "1wk", "1mo", "3mo", "1h", "90m", "60m", "30m", "15m", "5m", "2m", "1m"}


def get_prices(
    tickers: Union[str, Iterable[str]],
    start: Optional[object] = None,
    end: Optional[object] = None,
    interval: str = "1d",
    price_field: str = "Adj Close",
) -> pd.DataFrame:
    """
    Download historical price data and return a DataFrame of prices.

    Returns:
      DataFrame with DatetimeIndex and columns = tickers (uppercase)
    """
    tickers_list = ensure_ticker_list(tickers)

    if not isinstance(interval, str) or interval.strip() == "":
        raise InvalidInputError("interval must be a non-empty string.")
    interval = interval.strip()

    if interval not in _ALLOWED_INTERVALS:
        raise InvalidInputError(f"Unsupported interval '{interval}'. Allowed: {sorted(_ALLOWED_INTERVALS)}")

    start_ts = parse_date(start, "start")
    end_ts = parse_date(end, "end")
    validate_date_range(start_ts, end_ts)

    if not isinstance(price_field, str) or not price_field.strip():
        raise InvalidInputError("price_field must be a non-empty string.")
    price_field = price_field.strip()

    try:
        df = yf.download(
            tickers=tickers_list,
            start=None if start_ts is None else start_ts.to_pydatetime(),
            end=None if end_ts is None else end_ts.to_pydatetime(),
            interval=interval,
            auto_adjust=False,
            progress=False,
            group_by="ticker",
            threads=True,
        )
    except Exception as e:
        raise DataDownloadError(f"yfinance download failed: {e}")

    if df is None or len(df) == 0:
        raise EmptyDataError("No data returned. Check tickers and date range.")

    # Normalize outputs to: columns=tickers, values=price_field
    # Single ticker: columns like ["Open","High","Low","Close","Adj Close","Volume"]
    if not isinstance(df.columns, pd.MultiIndex):
        if price_field not in df.columns:
            raise EmptyDataError(f"Missing '{price_field}' in downloaded data.")
        out = df[[price_field]].copy()
        out.columns = [tickers_list[0]]
        out.index = pd.to_datetime(out.index)
        out = out.sort_index()
        out = out.dropna(how="all")
        if out.empty:
            raise EmptyDataError("All values are NaN after cleaning.")
        return out

    # Multi ticker: columns MultiIndex. With group_by="ticker": first level is ticker.
    prices = {}
    for t in tickers_list:
        if t not in df.columns.get_level_values(0):
            continue
        sub = df[t]
        if price_field not in sub.columns:
            continue
        s = sub[price_field].copy()
        prices[t] = s

    if not prices:
        raise EmptyDataError(f"No '{price_field}' data found for requested tickers.")

    out = pd.DataFrame(prices)
    out.index = pd.to_datetime(out.index)
    out = out.sort_index()
    out = out.dropna(how="all")
    if out.empty:
        raise EmptyDataError("All values are NaN after cleaning.")
    return out
