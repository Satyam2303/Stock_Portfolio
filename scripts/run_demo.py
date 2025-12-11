from stockscope.fetch import get_prices
from stockscope.indicators import daily_returns, sma, rsi
from stockscope.risk import volatility, max_drawdown, value_at_risk
from stockscope.portfolio import normalize_weights, buy_and_hold_value, portfolio_returns
from stockscope.plotting import plot_price_with_sma, plot_drawdown

def main():
    tickers = ["AAPL", "MSFT", "GOOGL"]
    prices = get_prices(tickers, start="2024-01-01", end="2024-12-31", interval="1d")

    # Indicators
    rets = daily_returns(prices)
    print("\nAnnualized volatility (252 trading days):")
    print(volatility(rets, annualize=True))

    # Risk + plotting for one ticker
    aapl = prices["AAPL"].dropna()
    dd = max_drawdown(aapl)
    print("\nAAPL worst drawdown:", float(dd.min()))

    aapl_rets = daily_returns(aapl).dropna()
    print("AAPL historical VaR(5%):", value_at_risk(aapl_rets, level=0.05))

    plot_price_with_sma(aapl, window=20, title="AAPL Price + 20D SMA")
    plot_drawdown(aapl, title="AAPL Drawdown")

    # Portfolio
    weights = normalize_weights({"AAPL": 0.4, "MSFT": 0.4, "GOOGL": 0.2})
    port_val = buy_and_hold_value(prices, weights, initial_value=10_000)
    port_rets = portfolio_returns(rets.dropna(how="all"), weights)

    print("\nPortfolio final value:", float(port_val.iloc[-1]))
    print("Portfolio annualized volatility:", float(volatility(port_rets, annualize=True)))

if __name__ == "__main__":
    main()
