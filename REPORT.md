# StockScope Project Report

## 1. Introduction
StockScope is a Python package designed for downloading stock price data and performing common analysis tasks such as computing indicators, risk metrics, simple portfolio performance, and visualizations. The package targets students and beginners who want a clean, reusable toolkit for finance-related analysis.

## 2. Package Design and Architecture
The package is split into focused modules:
- fetch.py: data download and cleaning from yfinance
- indicators.py: returns, SMA, EMA, RSI
- risk.py: volatility, max drawdown, historical VaR
- portfolio.py: weight normalization, portfolio returns, buy-and-hold value
- plotting.py: matplotlib plotting utilities
- exceptions.py: custom exceptions for user-friendly errors
- utils.py: shared validation helpers

This modular design improves readability and makes the package easy to extend.

## 3. Key Functionalities (3+)
1) Download prices for one or multiple tickers using yfinance, returning a clean DataFrame of prices.
2) Compute indicators such as daily returns, SMA, EMA, and RSI.
3) Compute risk metrics including annualized volatility, max drawdown, and historical VaR.
4) Portfolio analysis: normalize weights and compute buy-and-hold portfolio value over time.
5) Visualization: plot price with SMA and plot drawdown.

## 4. Error Handling Strategy
Potential user errors and solutions:
- Invalid ticker types or empty tickers -> InvalidInputError
- Invalid dates or start > end -> InvalidInputError
- yfinance failures (network or API) -> DataDownloadError
- Empty or unusable data returned -> EmptyDataError

All errors include human-readable messages to help users fix inputs quickly.

## 5. Testing Strategy
Unit tests were written using Python’s built-in unittest framework to validate:
- Indicator calculations return correct types and non-empty outputs
- Risk functions handle valid inputs and raise errors for invalid parameters
- Portfolio utilities properly normalize weights and reject missing tickers
- Utility functions reject invalid date formats and invalid ticker lists

Tests avoid relying on live yfinance calls to keep them stable and reproducible.

## 6. Challenges and Solutions
- yfinance may return different column formats for single vs multiple tickers (MultiIndex vs flat columns).
  Solution: normalize outputs into a DataFrame of price_field values with tickers as columns.
- Missing values and inconsistent trading days.
  Solution: drop all-NaN rows; forward fill only when needed for buy-and-hold initial prices.

## 7. Future Improvements
- Add more indicators (MACD, Bollinger Bands)
- Add optional caching to avoid repeated downloads
- Add more portfolio strategies (periodic rebalancing)
