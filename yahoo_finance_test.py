import unittest
import yahoo_finance

class TestSum(unittest.TestCase):
    def test_stock_info_from_yahoo(self):

        stock = yahoo_finance.get_stock_history("WKHS","5m")
        print(stock)
        self.assertIsNotNone(stock)

if __name__ == '__main__':
    unittest.main()