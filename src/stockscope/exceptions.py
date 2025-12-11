class StockScopeError(Exception):
    """Base exception for stockscope."""


class InvalidInputError(StockScopeError):
    """Raised when user inputs are invalid (types, ranges, dates, etc.)."""


class DataDownloadError(StockScopeError):
    """Raised when data download fails (yfinance/network)."""


class EmptyDataError(StockScopeError):
    """Raised when downloaded data is empty or missing required fields."""
