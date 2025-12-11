import unittest
import pandas as pd
import numpy as np

from stockscope.indicators import daily_returns, sma, ema, rsi
from stockscope.exceptions import InvalidInputError


class TestIndicators(unittest.TestCase):
    def setUp(self):
        idx = pd.date_range("2024-01-01", periods=5, freq="D")
        self.s = pd.Series([100, 101, 102, 100, 103], index=idx)

    def test_daily_returns(self):
        r = daily_returns(self.s)
        self.assertEqual(len(r), 4)

    def test_sma(self):
        m = sma(self.s, window=2)
        self.assertTrue(isinstance(m, pd.Series))

    def test_ema(self):
        m = ema(self.s, span=2)
        self.assertTrue(isinstance(m, pd.Series))

    def test_rsi(self):
        val = rsi(self.s, window=2)
        self.assertTrue(isinstance(val, pd.Series))

    def test_invalid_window(self):
        with self.assertRaises(InvalidInputError):
            sma(self.s, window=0)


if __name__ == "__main__":
    unittest.main()
