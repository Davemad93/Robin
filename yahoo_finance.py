import yfinance as yf
import time
import datetime as date
from datetime import timedelta

def get_stock_history(stock_name, interval):
    stock = yf.Ticker(stock_name)

    today = date.datetime.today()
    sixty_days_before = (today-timedelta(days=60))

    hist = stock.history(interval=interval, start=sixty_days_before, end=today, prepost="True")

    return hist["Close"][:-1]
