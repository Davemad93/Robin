class User:
    def __init__(self, wallet, num_of_stocks, stock_total, percent_total, num_of_trades, bought_date):
        self.wallet = wallet
        self.num_of_stocks = num_of_stocks
        self.stock_total = stock_total
        self.percent_total = percent_total
        self.num_of_trades = num_of_trades
        self.bought_date = bought_date

    def __str__(self):
        return 'wallet= {self.wallet}\nnum_of_stocks= {self.num_of_stocks}\nstock_total= {self.stock_total}\npercent_total= {self.percent_total}\nnum_of_trades= {self.num_of_trades}\n'.format(
            self=self)