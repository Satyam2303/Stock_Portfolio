import unittest
from stockscope.utils import ensure_ticker_list, parse_date, validate_date_range
from stockscope.exceptions import InvalidInputError


class TestUtils(unittest.TestCase):
    def test_ensure_ticker_list_str(self):
        self.assertEqual(ensure_ticker_list("aapl"), ["AAPL"])

    def test_ensure_ticker_list_csv(self):
        self.assertEqual(ensure_ticker_list("AAPL, msft"), ["AAPL", "MSFT"])

    def test_bad_date(self):
        with self.assertRaises(InvalidInputError):
            parse_date("2024-99-99", "start")

    def test_date_range(self):
        s = parse_date("2024-02-01", "start")
        e = parse_date("2024-01-01", "end")
        with self.assertRaises(InvalidInputError):
            validate_date_range(s, e)


if __name__ == "__main__":
    unittest.main()
