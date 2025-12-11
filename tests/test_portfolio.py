import unittest
import pandas as pd

from stockscope.portfolio import normalize_weights, buy_and_hold_value, portfolio_returns
from stockscope.exceptions import InvalidInputError


class TestPortfolio(unittest.TestCase):
    def setUp(self):
        idx = pd.date_range("2024-01-01", periods=4, freq="D")
        self.prices = pd.DataFrame(
            {"AAPL": [100, 101, 102, 103], "MSFT": [200, 198, 201, 202]},
            index=idx
        )
        self.rets = self.prices.pct_change().dropna()

    def test_normalize(self):
        w = normalize_weights({"AAPL": 2, "msft": 2})
        self.assertAlmostEqual(sum(w.values()), 1.0, places=8)

    def test_buy_and_hold(self):
        w = normalize_weights({"AAPL": 0.5, "MSFT": 0.5})
        pv = buy_and_hold_value(self.prices, w, initial_value=1000)
        self.assertEqual(len(pv), len(self.prices))

    def test_portfolio_returns(self):
        w = normalize_weights({"AAPL": 0.5, "MSFT": 0.5})
        pr = portfolio_returns(self.rets, w)
        self.assertEqual(len(pr), len(self.rets))

    def test_missing_ticker(self):
        w = normalize_weights({"TSLA": 1.0})
        with self.assertRaises(InvalidInputError):
            buy_and_hold_value(self.prices, w, 1000)


if __name__ == "__main__":
    unittest.main()
