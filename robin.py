from pyrh import Robinhood
from user import User
import config
import numpy as np
import tulipy as ti
import yahoo_finance
import robinhood_function, pyotp
import asyncio
import time

# Log in to Robinhood app (will prompt for two-factor)
rh = Robinhood()
rh.login(username=config.USERNAME,
         password=config.PASSWORD,
         qr_code=config.MFA)

# Set some variables
stock_ticker = input("\nEnter Stock ticker you would like to trade: ").upper()
shares_to_buy = input("Enter amount of shares to purchase: ")

# Create a User
user = User(rh, stock_ticker, shares_to_buy)

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
        [close_prices.append(float(key['close_price'])) for key in day_year_quotes["results"][0]["historicals"]]

        # Manually insert LATEST TRADE PRICE to CLOSE PRICES to calculate RSI better.
        close_prices.append(float(user.latest_trade_price))

        # Create Numpy DataFrame
        DAILY_DATA = np.array(close_prices)
        FIVEMIN_DATA = np.array(five_min_day_yahoo)

        # Get stock instrument
        instrument = rh.instruments(stock_ticker)[0]

        # Calculate Indicator - maybe try rsi 10/14 for daily
        indicator_period = 3
        rsi = ti.rsi(DAILY_DATA, period=indicator_period)
        rsi_5 = ti.rsi(FIVEMIN_DATA, period=indicator_period)

        trade_logic_data = {'RSI':rsi, "RSI_5":rsi_5, }

        print("Previous daily RSIs")
        get_list_of_rsi(DAILY_DATA, rsi)
        print("-----------------------")
        print("Previous 5 minute RSIs")
        get_list_of_rsi(FIVEMIN_DATA, rsi_5)

        print("\nCURRENT DAILY RSI--{}%".format(rsi[-1]))
        print(user)

        ## BUYING LOGIC
        robinhood_function.buy_stock(trade_logic_data, instrument, user, rh)

        ## SELLING LOGIC
        robinhood_function.sell_stock(trade_logic_data, instrument, user, rh)

        # Call this method again every 5 minutes for new price changes
        print()
        print()
        await asyncio.sleep(config.SLEEP)

def get_list_of_rsi(data_type, rsi_type):
    return [print("CLOSE: ${} RSI: {}%".format(data_type[-x], rsi_type[-x])) for x in range(1, 11)]


loop = asyncio.get_event_loop()
loop.create_task(run())
loop.run_forever()

if __name__ == '__main__':
    run()
