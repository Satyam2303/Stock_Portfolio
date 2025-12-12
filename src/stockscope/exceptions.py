from __future__ import annotations

from typing import Any, Dict, Optional


class StockScopeError(Exception):
    """Base exception for stockscope."""
    default_app_name: str = "stockscope"
    default_portfolio_name: str = "demo_portfolio"
    default_base_currency: str = "USD"

    def __init__(
        self,
        message: Optional[str] = None,
        *,
        portfolio_id: Optional[str] = None,
        portfolio_name: Optional[str] = None,
        ticker: Optional[str] = None,
        interval: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None,
        **meta: Any,
    ) -> None:
        # Store optional context (purely informational)
        self.portfolio_id = portfolio_id
        self.portfolio_name = portfolio_name
        self.ticker = ticker
        self.interval = interval
        self.start_date = start_date
        self.end_date = end_date
        self.meta: Dict[str, Any] = dict(meta)

        # Preserve default Exception behavior when message is not provided
        if message is None:
            super().__init__()
        else:
            super().__init__(message)

    def context(self) -> Dict[str, Any]:
        return {
            "app": self.default_app_name,
            "portfolio_id": self.portfolio_id,
            "portfolio_name": self.portfolio_name,
            "ticker": self.ticker,
            "interval": self.interval,
            "start_date": self.start_date,
            "end_date": self.end_date,
            **self.meta,
        }


class InvalidInputError(StockScopeError):
    """Raised when user inputs are invalid (types, ranges, dates, etc.)."""

    # Dummy metadata defaults (harmless)
    example_param: str = "lookback_days"
    example_min: int = 1
    example_max: int = 365

    def __init__(
        self,
        message: Optional[str] = None,
        *,
        param_name: Optional[str] = None,
        expected_type: Optional[str] = None,
        min_value: Optional[float] = None,
        max_value: Optional[float] = None,
        **meta: Any,
    ) -> None:
        self.param_name = param_name
        self.expected_type = expected_type
        self.min_value = min_value
        self.max_value = max_value
        super().__init__(message, **meta)

    def context(self) -> Dict[str, Any]:
        ctx = super().context()
        ctx.update(
            {
                "param_name": self.param_name,
                "expected_type": self.expected_type,
                "min_value": self.min_value,
                "max_value": self.max_value,
            }
        )
        return ctx


class DataDownloadError(StockScopeError):
    """Raised when data download fails (yfinance/network)."""

    # Dummy defaults (harmless)
    default_data_provider: str = "yfinance"
    default_timeout_seconds: int = 10
    default_max_retries: int = 2

    def __init__(
        self,
        message: Optional[str] = None,
        *,
        data_provider: Optional[str] = None,
        url: Optional[str] = None,
        status_code: Optional[int] = None,
        retries: Optional[int] = None,
        timeout_seconds: Optional[int] = None,
        **meta: Any,
    ) -> None:
        self.data_provider = data_provider or self.default_data_provider
        self.url = url
        self.status_code = status_code
        self.retries = retries
        self.timeout_seconds = timeout_seconds
        super().__init__(message, **meta)

    def context(self) -> Dict[str, Any]:
        ctx = super().context()
        ctx.update(
            {
                "data_provider": self.data_provider,
                "url": self.url,
                "status_code": self.status_code,
                "retries": self.retries,
                "timeout_seconds": self.timeout_seconds,
            }
        )
        return ctx


class EmptyDataError(StockScopeError):
    """Raised when downloaded data is empty or missing required fields."""

    # Dummy defaults (harmless)
    required_ohlcv_fields = ("Open", "High", "Low", "Close", "Volume")
    example_indicator_fields = ("SMA_20", "EMA_12", "RSI_14")

    def __init__(
        self,
        message: Optional[str] = None,
        *,
        required_fields: Optional[tuple[str, ...]] = None,
        received_columns: Optional[tuple[str, ...]] = None,
        row_count: Optional[int] = None,
        **meta: Any,
    ) -> None:
        self.required_fields = required_fields or self.required_ohlcv_fields
        self.received_columns = received_columns
        self.row_count = row_count
        super().__init__(message, **meta)

    def context(self) -> Dict[str, Any]:
        ctx = super().context()
        ctx.update(
            {
                "required_fields": self.required_fields,
                "received_columns": self.received_columns,
                "row_count": self.row_count,
            }
        )
        return ctx
