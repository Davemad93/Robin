import unittest
import database_function


database = "database.txt"

class TestSum(unittest.TestCase):
    def test_get_number_of_trades_from_database(self):
        number_of_trades = database_function.get_number_of_trades(database)
        self.assertEquals(3, int(number_of_trades))
    
    def test_update_number_of_trades_in_database(self):
        trade_number = 1
        database_function.update_trade_number(str(trade_number), database)
        number_of_trades = database_function.get_number_of_trades(database)
        self.assertEquals(1, int(number_of_trades))

if __name__ == '__main__':
    unittest.main()