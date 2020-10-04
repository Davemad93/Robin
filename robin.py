from pyrh import Robinhood
from datetime import datetime
import config
import numpy as np
import tulipy as ti
import yahoo_finance
import sched, time
import pyotp
import robinhood_function
# import asyncio


# Log in to Robinhood app (will prompt for two-factor)
rh = Robinhood()
rh.login(username=config.USERNAME,
         password=config.PASSWORD,
         qr_code=config.MFA)

#Setup some variables
entered_trade = False

# STOCK TICKER
stock_ticker = "WKHS"

# Get quote data from RH API
day_year_quotes = rh.get_historical_quotes(stock_ticker, 'day', 'year')

#Initiate our scheduler so we can keep checking every minute for new price changes
s = sched.scheduler(time.time, time.sleep)

def run(sc):
    # while True:
    global entered_trade
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime())

    # POST TIME
    print("Getting historical quotes on {}".format(time_string))

    # This gets the last 60 days including today.
    five_min_day_yahoo = yahoo_finance.get_stock_history(stock_ticker, "5m")

    # Create list of closing prices from RH API
    close_prices = []
    for key in day_year_quotes["results"][0]["historicals"]:
        close_prices.append(float(key['close_price']))

    # Create Numpy DataFrame
    DAILY_DATA = np.array(close_prices)
    FIVEMIN_DATA = np.array(five_min_day_yahoo)

    # Get stock instrument
    instrument = rh.instruments(stock_ticker)[0]

    # Calculate Indicator
    indicator_period = 3
    rsi = ti.rsi(DAILY_DATA, period=indicator_period)
    rsi_5 = ti.rsi(FIVEMIN_DATA, period=indicator_period)

    trade_logic_data = {'RSI':rsi, "RSI_5":rsi_5, "fivemin_close_prices":FIVEMIN_DATA }

    rsi[-1] = 17
    ## BUYING LOGIC 
    robinhood_function.buy_stock(trade_logic_data, entered_trade, FIVEMIN_DATA, instrument)

    ## SELLING LOGIG
    robinhood_function.sell_stock(trade_logic_data, entered_trade, FIVEMIN_DATA, instrument)

    #call this method again every 5 minutes for new price changes
    s.enter(300, 1, run, (sc, ))
    # await asyncio.sleep(300)


s.enter(1, 1, run, (s, ))
s.run()

if __name__ == '__main__':
    run()


# loop = asyncio.get_event_loop()
# loop.create_task(runner())
# loop.run_forever()