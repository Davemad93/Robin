import yfinance as yf
import time

# https://algotrading101.com/learn/yfinance-guide/

def get_stock_history(stock_name, time_period, interval):
    stock = yf.Ticker(stock_name)

    # get historical market data
    #         interval: data interval (1m data is only for available for last 7 days, and data interval <1d for the last 60 days) Valid intervals are:
    # “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”
    hist = stock.history(period=time_period, interval=interval)

    # time.sleep(1)
    return hist["Close"]