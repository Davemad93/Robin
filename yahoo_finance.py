import yfinance as yf
import time
import datetime as date
from datetime import timedelta

# https://algotrading101.com/learn/yfinance-guide/

def get_stock_history(stock_name, time_period, interval):
    stock = yf.Ticker(stock_name)

    # get historical market data
    #         interval: data interval (1m data is only for available for last 7 days, and data interval <1d for the last 60 days) Valid intervals are:
    # “1m”, “2m”, “5m”, “15m”, “30m”, “60m”, “90m”, “1h”, “1d”, “5d”, “1wk”, “1mo”, “3mo”

    today = date.datetime.today()
    sixty_days_before = (today-timedelta(days=60))

    #print(str(today).split(" ")[0])
    #print(str(sixty_days_before).split(" ")[0])

    hist = stock.history(interval="5m", start=sixty_days_before, end=today, prepost="True")
    #print(hist)

    # time.sleep(1)
    return hist["Close"]
