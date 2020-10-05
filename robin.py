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

# STOCK TICKER
stock_ticker = input("Enter Stock ticker you would like to trade: ").upper() # This needs to be caps

user = User(0,0,0,0,0,None)

# Get quote data from RH API
day_year_quotes = rh.get_historical_quotes(stock_ticker, 'day', 'year')
#print(* day_year_quotes["results"][0]["historicals"], sep='\n')

async def run():
    while True:
        time_string = time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime())

        # POST TIME
        print("\nGetting historical quotes on {}".format(time_string))

        # This gets the last 60 days including today.
        five_min_day_yahoo = yahoo_finance.get_stock_history(stock_ticker, "5m")

        # Create list of closing prices from RH API
        close_prices = []
        for key in day_year_quotes["results"][0]["historicals"]:
            close_prices.append(float(key['close_price']))

        # Get stock quote
        quote_data = rh.get_quote(stock_ticker)

        # Manually insert LATEST TRADE PRICE to CLOSE PRICES to calculate RSI better.
        #print(quote_data)
        if datetime.now().hour >= 15:
            latest_trade_price = float(quote_data['last_extended_hours_trade_price'])
        else:
            latest_trade_price = float(quote_data['last_trade_price'])

        # Create Numpy DataFrame
        DAILY_DATA = np.array(close_prices)
        FIVEMIN_DATA = np.array(five_min_day_yahoo)

        # Get stock instrument
        instrument = rh.instruments(stock_ticker)[0]

        # Calculate Indicator
        indicator_period = 3
        rsi = ti.rsi(DAILY_DATA, period=indicator_period)
        rsi_5 = ti.rsi(FIVEMIN_DATA, period=indicator_period)

        trade_logic_data = {"LTP": str(latest_trade_price), 'RSI':rsi, "RSI_5":rsi_5, }

        print("Previous daily RSIs")
        for x in range(1, 11):
            print("CLOSE: {} RSI: {}".format(DAILY_DATA[-x], rsi[-x]))

        print("Previous 5 minute RSIs")
        for x in range(1, 11):
            print("CLOSE: {} RSI: {}".format(FIVEMIN_DATA[-x], rsi_5[-x]))

        ## BUYING LOGIC 
        robinhood_function.buy_stock(trade_logic_data, instrument, user, rh, quote_data)

        ## SELLING LOGIG
        robinhood_function.sell_stock(trade_logic_data, instrument, user, rh, quote_data)

        # Call this method again every 5 minutes for new price changes
        await asyncio.sleep(15)

loop = asyncio.get_event_loop()
loop.create_task(run())
loop.run_forever()

if __name__ == '__main__':
    run()
