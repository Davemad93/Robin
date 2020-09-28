from pyrh import Robinhood
from datetime import datetime
import config
import numpy as np
import tulipy as ti
import sched
import time
import pyotp

#A Simple Robinhood Python Trading Bot using RSI (buy <=30 and sell >=70 RSI) and with support and resistance.
#totp = pyotp.TOTP("").now()
#print(totp)

# Log in to Robinhood app (will prompt for two-factor)
rh = Robinhood()
rh.login(username=config.USERNAME, password=config.PASSWORD,  qr_code=config.MFA)

#Setup our variables, we haven't entered a trade yet and our RSI period
enteredTrade = False
dayPeriod = 251

#Initiate our scheduler so we can keep checking every minute for new price changes
s = sched.scheduler(time.time, time.sleep)

def run(sc): 
    global enteredTrade
    global dayPeriod
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime())

    print("Getting historical quotes on {}".format(time_string))
    stock_ticker = "WKHS"
    historical_quotes = rh.get_historical_quotes(stock_ticker, 'day', 'year') # Currently getting years worth of data by day. 251 days worth.
    closePrices = []

    # Get all closing prices.
    for key in historical_quotes["results"][0]["historicals"]:
        closePrices.append(float(key['close_price']))

    DATA = np.array(closePrices)

    if (len(closePrices) >= (dayPeriod)):
        #Calculate Indicators
        indicator_period = 3
        rsi = ti.rsi(DATA, period=indicator_period) # Currently only using this one
        sma = ti.sma(DATA, period=indicator_period)
        ema = ti.ema(DATA, period=indicator_period)
        instrument = rh.instruments(stock_ticker)[0]

        # Extra variables that are not being used. Just saving. 
        previousClosePrice = rh.previous_close(stock_ticker)  # yesterdays close price
        lastTradePrice = rh.last_trade_price(stock_ticker)   # last trade price i think is 8pm\7:55pm
        lastExtendedHoursPrice = rh.get_quote(stock_ticker)['last_extended_hours_trade_price'] 

        ## BUYING LOGIC
        #If rsi is less than or equal to 20 buy
        #if rsi[len(rsi) - 1] <= 20 and float(key['close_price']) <= currentSupport and not enteredTrade:
        five_recent_rsi = {}
        if rsi[-1] <= 20 and not enteredTrade: # and not enterTrade means we will not buy again after we bought in for this trade. This is typically for long positions, remove this for short pos
            print("RSI is below 20! Send signal that it may be time to buy / move into next stage of program which utilized 5minute:day chart instead of day:year chart to do so")

            print("Previous 5 RSIs")
            for x in range(1,6):
                date = historical_quotes["results"][0]["historicals"][-x]['begins_at']
                #five_recent_rsi[date] = rsi[-x]
                print("Date: {} RSI: {}".format(date,rsi[-x]))

            # Market buy order, not a limit order.
            #rh.place_buy_order(instrument, 10)
            #enteredTrade = True


        ## SELLING LOGIC
        #Sell when RSI reaches 80
        if rsi[-1] >= 80 and enteredTrade:
            print("RSI is above 80! Send signal that it may be time to sell / move into next stage and find a nice price to sell at. Utilize 5minute:day chart to do so")

            print("Previous 5 RSIs")
            for x in range(1,6):
                date = historical_quotes["results"][0]["historicals"][-x]['begins_at']
                #five_recent_rsi[date] = rsi[-x]
                print("Date: {} RSI: {}".format(date,rsi[-x]))

            # Market buy order, not a limit order.
            #rh.place_sell_order(instrument, 10)
            #enteredTrade = False


    #call this method again every 5 minutes for new price changes
    s.enter(300, 1, run, (sc,))

s.enter(1, 1, run, (s,))
s.run()


    
# takes in two numbers and gives back the percent difference wheather it be an increase or decrease. 
def calculate_percent_difference(prev_num, curr_num):
    if curr_num > prev_num: # This is a percent increase
        increase = float(curr_num) - float(prev_num)
        percent_increase = (increase / float(prev_num)) * 100 
        return "The percent increase is: {}".format(percent_increase) # if number is negative then this is a percent decrease
    elif curr_num < prev_num:
        decrease = float(prev_num) - float(curr_num)
        percent_decrease = (decrease / float(prev_num)) * 100
        return "The percent decrease is: {}".format(percent_decrease) # if answer is negative then this is a percent increase
    elif curr_num == prev_num:
        return "curr_num and prev_num are equal."
    else: 
        return "Some error occured, mayday!!!!"

