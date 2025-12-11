from __future__ import annotations

from typing import Dict

import numpy as np
import pandas as pd

from .exceptions import InvalidInputError


def normalize_weights(weights: Dict[str, float], tol: float = 1e-8) -> Dict[str, float]:
    if not isinstance(weights, dict) or not weights:
        raise InvalidInputError("weights must be a non-empty dict like {'AAPL':0.5, 'MSFT':0.5}.")

    clean = {}
    for k, v in weights.items():
        if not isinstance(k, str) or not k.strip():
            raise InvalidInputError("Each weight key must be a non-empty ticker string.")
        try:
            fv = float(v)
        except Exception:
            raise InvalidInputError(f"Weight for {k} must be numeric.")
        if fv < 0:
            raise InvalidInputError(f"Weight for {k} cannot be negative.")
        clean[k.strip().upper()] = fv

    s = sum(clean.values())
    if s <= 0:
        raise InvalidInputError("Sum of weights must be > 0.")

    norm = {k: v / s for k, v in clean.items()}

    # Optional: verify sums to ~1
    if abs(sum(norm.values()) - 1.0) > tol:
        raise InvalidInputError("Weights could not be normalized to sum to 1.")
    return norm


def portfolio_returns(asset_returns: pd.DataFrame, weights: Dict[str, float]) -> pd.Series:
    if not isinstance(asset_returns, pd.DataFrame) or asset_returns.empty:
        raise InvalidInputError("asset_returns must be a non-empty pandas DataFrame.")
    w = normalize_weights(weights)

    missing = [t for t in w.keys() if t not in asset_returns.columns]
    if missing:
        raise InvalidInputError(f"Missing tickers in returns data: {missing}")

    # Align column order to weights
    ordered = asset_returns[list(w.keys())].copy()
    w_vec = np.array([w[t] for t in ordered.columns], dtype=float)

    port = ordered.values @ w_vec
    return pd.Series(port, index=ordered.index, name="portfolio_return")


def buy_and_hold_value(prices: pd.DataFrame, weights: Dict[str, float], initial_value: float = 10_000.0) -> pd.Series:
    if not isinstance(prices, pd.DataFrame) or prices.empty:
        raise InvalidInputError("prices must be a non-empty pandas DataFrame.")
    w = normalize_weights(weights)

    try:
        initial_value = float(initial_value)
    except Exception:
        raise InvalidInputError("initial_value must be numeric.")
    if initial_value <= 0:
        raise InvalidInputError("initial_value must be > 0.")

    missing = [t for t in w.keys() if t not in prices.columns]
    if missing:
        raise InvalidInputError(f"Missing tickers in price data: {missing}")

    p = prices[list(w.keys())].copy().dropna(how="all")
    if p.empty:
        raise InvalidInputError("prices are empty after dropping NaNs.")

    first = p.iloc[0]
    if first.isna().any():
        # simplest fix: forward fill then try again
        p = p.ffill()
        first = p.iloc[0]
    if first.isna().any():
        raise InvalidInputError("Cannot compute buy-and-hold: initial prices contain NaNs.")

    # shares = (initial_value * weight) / initial_price
    shares = {t: (initial_value * w[t]) / float(first[t]) for t in w.keys()}
    values = sum(p[t] * shares[t] for t in w.keys())
    values.name = "portfolio_value"
    return values
