import database_function
import robinhood_function
from datetime import datetime

class User:
    def __init__(self, rh, ticker, shares_to_buy):
        self.shares_to_buy = shares_to_buy
        self.stock_ticker = ticker
        self.bought_date = None

        self.day_trades = int(database_function.get_number_of_trades("database.txt"))
        self.buying_power = float(rh.portfolios()["withdrawable_amount"])

        self.shares_owned = get_shares_owned(self,rh,ticker)
        self.average = get_average(self,rh,ticker)
        self.latest_trade_price = get_last_sp(self, rh, ticker)

        self.total_equity = self.average * self.shares_owned
        self.estimated_trans_cost = self.latest_trade_price * self.shares_owned
        self.gainsloses = round((self.latest_trade_price *  self.shares_owned) - self.total_equity,2)


    def __str__(self):
        return '\nPortfolio info:\
                \nbuying_power= ${self.buying_power}\
                \nday_trades= {self.day_trades}\
                \nshares_owned= {self.shares_owned}\
                \naverage= ${self.average}\
                \ntotal_equity= ${self.total_equity}\
                \n\
                \nTransaction info: \
                \nstock_ticker= {self.stock_ticker}\
                \nshares_to_buy= {self.shares_to_buy}\
                \nlatest_trade_price= ${self.latest_trade_price}\
                \nestimated_trans_cost= ${self.estimated_trans_cost}\
                \nGains/Loses= ${self.gainsloses}\n'.format(self=self)


def get_average(self, rh, stock_ticker):
    url = "https://api.robinhood.com/positions"
    pos_id = rh.instruments(stock_ticker)[0]['id']
    account = rh.positions()['results'][0]['account_number']
    url = "{}/{}/{}/".format(url, account, pos_id)
    for x in rh.positions()['results']:
        if x["url"] == url: # Checks if we have made a trade yet
            average = x['average_buy_price']
            return float(average)
        else:
            #print("We do not have an open position with {}. Setting avg to 0.0".format(stock_ticker))
            return 0.0

def get_shares_owned(self, rh, stock_ticker):
    url = "https://api.robinhood.com/positions"
    pos_id = rh.instruments(stock_ticker)[0]['id']
    account = rh.positions()['results'][0]['account_number']
    url = "{}/{}/{}/".format(url, account, pos_id)
    for x in rh.positions()['results']:
        if x["url"] == url:
            shares_owned = x['quantity']
            return float(shares_owned)
        else:
            #print("We do not have an open position with {}. Setting shares owned to 0".format(stock_ticker))
            return 0.0

def get_last_sp(self, rh, ticker):
    print("Getting latest trade price")
    # Get stock quote
    quote_data = rh.get_quote(ticker)
    if datetime.now().hour >= 15:
       return float(quote_data['last_extended_hours_trade_price'])
    else:
       return float(quote_data['last_trade_price'])
