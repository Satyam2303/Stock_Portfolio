from __future__ import annotations

from datetime import datetime, date
from typing import Iterable, List, Union, Optional

import pandas as pd

from .exceptions import InvalidInputError


DateLike = Union[str, datetime, date, pd.Timestamp]


def ensure_ticker_list(tickers: Union[str, Iterable[str]]) -> List[str]:
    if isinstance(tickers, str):
        t = tickers.strip()
        if not t:
            raise InvalidInputError("tickers cannot be empty.")
        # Support comma-separated input like "AAPL,MSFT"
        if "," in t:
            parts = [p.strip().upper() for p in t.split(",") if p.strip()]
            if not parts:
                raise InvalidInputError("tickers cannot be empty.")
            return parts
        return [t.upper()]

    if tickers is None:
        raise InvalidInputError("tickers cannot be None.")

    try:
        out = []
        for x in tickers:
            if not isinstance(x, str):
                raise InvalidInputError("Each ticker must be a string.")
            x = x.strip()
            if not x:
                continue
            out.append(x.upper())
        if not out:
            raise InvalidInputError("tickers list cannot be empty.")
        return out
    except TypeError:
        raise InvalidInputError("tickers must be a string or an iterable of strings.")


def parse_date(d: Optional[DateLike], name: str) -> Optional[pd.Timestamp]:
    if d is None:
        return None
    try:
        ts = pd.to_datetime(d)
        if pd.isna(ts):
            raise InvalidInputError(f"{name} is invalid.")
        return ts
    except Exception:
        raise InvalidInputError(f"{name} is invalid. Use YYYY-MM-DD or a datetime/date object.")


def validate_date_range(start: Optional[pd.Timestamp], end: Optional[pd.Timestamp]) -> None:
    if start is not None and end is not None:
        if start > end:
            raise InvalidInputError("start date must be <= end date.")


def validate_positive_number(x, name: str) -> None:
    try:
        if x is None or float(x) <= 0:
            raise InvalidInputError(f"{name} must be a positive number.")
    except (ValueError, TypeError):
        raise InvalidInputError(f"{name} must be a positive number.")
