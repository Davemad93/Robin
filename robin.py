from pyrh import Robinhood
from datetime import datetime
import config
import numpy as np
import tulipy as ti
import yahoo_finance
import sched, time
import pyotp
import robinhood_function
import asyncio
from user import User

# Log in to Robinhood app (will prompt for two-factor)
rh = Robinhood()
rh.login(username=config.USERNAME,
         password=config.PASSWORD,
         qr_code=config.MFA)

#Setup some variables
entered_trade = False

# STOCK TICKER
stock_ticker = "SUNW"

user = User(0,0,0,0,3,None)

# Get quote data from RH API
day_year_quotes = rh.get_historical_quotes(stock_ticker, 'day', 'year')

async def run():
    while True:
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
        print(instrument)

        # Calculate Indicator
        indicator_period = 3
        rsi = ti.rsi(DAILY_DATA, period=indicator_period)
        rsi_5 = ti.rsi(FIVEMIN_DATA, period=indicator_period)

        trade_logic_data = {'RSI':rsi, "RSI_5":rsi_5, "fivemin_close_prices":FIVEMIN_DATA }

        ## BUYING LOGIC 
        robinhood_function.buy_stock(trade_logic_data, entered_trade, FIVEMIN_DATA, instrument, user, rh)

        ## SELLING LOGIG
        robinhood_function.sell_stock(trade_logic_data, entered_trade, FIVEMIN_DATA, instrument, user, rh)

        #call this method again every 5 minutes for new price changes
        await asyncio.sleep(300)

loop = asyncio.get_event_loop()
loop.create_task(run())
loop.run_forever()

if __name__ == '__main__':
    run()