import unittest
import pandas as pd
import numpy as np

from stockscope.risk import volatility, max_drawdown, value_at_risk
from stockscope.exceptions import InvalidInputError


class TestRisk(unittest.TestCase):
    def setUp(self):
        idx = pd.date_range("2024-01-01", periods=6, freq="D")
        self.prices = pd.Series([100, 110, 105, 120, 90, 95], index=idx)
        self.rets = self.prices.pct_change().dropna()

    def test_volatility(self):
        v = volatility(self.rets, annualize=False)
        self.assertTrue(float(v) >= 0)

    def test_drawdown(self):
        dd = max_drawdown(self.prices)
        self.assertEqual(len(dd), len(self.prices))
        self.assertTrue(dd.min() <= 0)

    def test_var(self):
        v = value_at_risk(self.rets, level=0.05)
        self.assertTrue(isinstance(v, float))

    def test_invalid_level(self):
        with self.assertRaises(InvalidInputError):
            value_at_risk(self.rets, level=1.5)


if __name__ == "__main__":
    unittest.main()
