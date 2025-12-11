# StockScope – 15 Minute Presentation Plan

## Slide 1: Title + Team Roles
- StockScope: Stock & Portfolio Analysis Python Package
- Team roles (module ownership)

## Slide 2: Problem & Motivation
- Students and beginners need reusable tools for finance analysis
- Avoid writing one-off notebooks every time

## Slide 3: Rules Compliance
- No linear regression package
- No ML / web
- Only pandas/numpy/matplotlib/datetime/yfinance

## Slide 4: Architecture
- fetch, indicators, risk, portfolio, plotting
- exceptions + utils for robustness

## Slide 5: Functionality Demo Roadmap
- Download prices -> indicators -> risk -> portfolio -> plots

## Slide 6: Fetch Module
- get_prices(tickers, start, end, interval)
- handles single vs multi ticker

## Slide 7: Indicators
- daily_returns, SMA, EMA, RSI
- show one plot: AAPL price + SMA(20)

## Slide 8: Risk
- volatility (annualized)
- max drawdown (plot)
- VaR(5%)

## Slide 9: Portfolio
- normalize weights
- buy-and-hold portfolio value

## Slide 10: Error Handling (Live)
- try bad ticker and show friendly error message

## Slide 11: Testing
- unittest coverage
- reproducible tests without live API dependency

## Slide 12: Summary + Future Work
- recap + next improvements

## Live Demo
Run:
python scripts/run_demo.py
