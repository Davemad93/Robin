import database_function
from datetime import datetime

class User:
    def __init__(self, rh, ticker, shares_to_buy):
        day_trades = int(database_function.get_number_of_trades("database.txt"))
        buying_power = float(rh.portfolios()["withdrawable_amount"])
        average_buy_price = get_average_price(self,rh,ticker)
        shares_owned = get_shares_owned(self,rh,ticker)
        equity =  float(average_buy_price) * shares_owned
        latest_trading_price = get_latest_trading_price(self,rh,ticker)
        gainsloses = round((float(latest_trading_price) * int(shares_owned)) - equity,2)
        estimated_trans_cost = (latest_trading_price * float(shares_to_buy))

        self.buying_power = buying_power
        self.shares_owned = shares_owned
        self.average_buy_price = average_buy_price
        self.total_equity = equity
        self.day_trades = day_trades
        self.bought_date = None
        self.shares_to_buy = shares_to_buy
        self.stock_ticker = ticker
        self.latest_trade_price = latest_trading_price
        self.estimated_trans_cost = estimated_trans_cost


    def __str__(self):
        return 'buying_power= {self.buying_power}\nshares_owned= {self.shares_owned}\naverage_buy_price= {self.average_buy_price}\ntotal_equity= {self.total_equity}\nday_trades= {self.day_trades}\nshares_to_buy= {self.shares_to_buy}\nstock_ticker= {self.stock_ticker}\nlatest_trade_price= {self.latest_trade_price}\nlatest_trade_price2= {self.get_latest_trading_price(self,rh,ticker)}\nestimated_trans_cost= {self.estimated_trans_cost}'.format(self=self)


def get_average_price(self, rh, stock_ticker):
    url = "https://api.robinhood.com/positions"
    pos_id = rh.instruments(stock_ticker)[0]['id']
    account = rh.positions()['results'][0]['account_number']
    url = "{}/{}/{}/".format(url, account, pos_id)
    for x in rh.positions()['results']:
        if x["url"] == url:
            average_buy_price = x['average_buy_price']
            return float(average_buy_price)

def get_shares_owned(self, rh, stock_ticker):
    url = "https://api.robinhood.com/positions"
    pos_id = rh.instruments(stock_ticker)[0]['id']
    account = rh.positions()['results'][0]['account_number']
    url = "{}/{}/{}/".format(url, account, pos_id)
    for x in rh.positions()['results']:
        if x["url"] == url:
            shares_owned = float(x['quantity'])
            return float(shares_owned)

def get_latest_trading_price(self, rh, ticker):
    # Get stock quote
    quote_data = rh.get_quote(ticker)

    if datetime.now().hour >= 15:
       return float(quote_data['last_extended_hours_trade_price'])
    else:
       return float(quote_data['last_trade_price'])
