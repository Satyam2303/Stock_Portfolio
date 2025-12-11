Team Members and Contributions

Aditya

Leads overall project setup and package structure (pyproject.toml, src/ layout).

Implements the data fetching and validation layer:

exceptions.py – custom exception classes for friendly error messages.

utils.py – input validation helpers (ticker parsing, date parsing, positive number checks).

fetch.py – get_prices() function to download and clean price data from yfinance.

Prepares basic usage examples and helps verify that all modules work together end-to-end.

Satyam

Implements the analysis and risk modules:

indicators.py – daily/log returns, SMA, EMA, RSI and related validation.

risk.py – volatility, max drawdown, historical Value at Risk (VaR).

portfolio.py – weight normalization, portfolio returns, and buy-and-hold portfolio value.

Develops and runs the unit tests:

tests/test_indicators.py, tests/test_risk.py, tests/test_portfolio.py, tests/test_utils_validation.py.

Ensures the numerical results are reasonable and consistent across the package.

Vishrutha

Responsible for visualization and communication:

plotting.py – plotting functions for price with SMA, drawdown, and portfolio value using matplotlib.

scripts/run_demo.py – demo script that ties together fetching, indicators, risk, portfolio, and plotting for the live presentation.

Leads documentation and presentation:

Writes and refines README.md (installation, quick start, module overview, error handling examples).

Organizes and edits REPORT.md and prepares PRESENTATION.md (slide structure, speaker notes).

Presents the live demo during the 15-minute presentation.