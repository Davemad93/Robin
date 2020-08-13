from pyrh import Robinhood
from datetime import datetime
import config
import numpy as np
import tulipy as ti
import sched
import time
import pyotp

#A Simple Robinhood Python Trading Bot using RSI (buy <=30 and sell >=70 RSI) and with support and resistance.

## DONALDS IS A BIG OL FAG!!!!

# Log in to Robinhood app (will prompt for two-factor)
totp = pyotp.TOTP(config.MFA).now()
#totp = pyotp.TOTP("867029").now()
rh = Robinhood()
rh.login(username=config.USERNAME,
         password=config.PASSWORD,
         qr_code=config.MFA)
#Setup our variables, we haven't entered a trade yet and our RSI period
enteredTrade = False
rsiPeriod = 200
#Initiate our scheduler so we can keep checking every minute for new price changes
s = sched.scheduler(time.time, time.sleep)
s1 = sched.scheduler(time.time, time.sleep)


def run(sc):
    global enteredTrade
    global rsiPeriod
    time_tuple = time.localtime()
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", time_tuple)
    print("Getting historical quotes on {}".format(time_string))
    # Get 5 minute bar data for a stock
    historical_quotes = rh.get_historical_quotes("WKHS", "day", "year")
    #print(historical_quotes)
    #   print(*historical_quotes["results"][0]["historicals"], sep='\n')
    closePrices = []
    #format close prices for RSI
    currentIndex = 0
    currentSupport = 0
    currentResistance = 0
    #print("Getting News")
    #print(rh.get_news("WKHS"))

    for key in historical_quotes["results"][0]["historicals"]:
        if (currentIndex >=
                len(historical_quotes["results"][0]["historicals"]) -
            (rsiPeriod + 1)):
            if (currentIndex >= (rsiPeriod - 1) and datetime.strptime(
                    key['begins_at'], '%Y-%m-%dT%H:%M:%SZ').minute == 0):
                currentSupport = 0
                currentResistance = 0
                print("Resetting support and resistance")
            if (float(key['close_price']) < currentSupport
                    or currentSupport == 0):
                currentSupport = float(key['close_price'])
                print("Current Support is : ")
                print(currentSupport)
            if (float(key['close_price']) > currentResistance):
                currentResistance = float(key['close_price'])
                print("Current Resistance is : ")
                print(currentResistance)
            closePrices.append(float(key['close_price']))
        currentIndex += 1
    DATA = np.array(closePrices)
    if (len(closePrices) > (rsiPeriod)):
        #Calculate RSI
        rsi = ti.rsi(DATA, period=rsiPeriod)
        sma = ti.sma(DATA, period=rsiPeriod)
        instrument = rh.instruments("F")[0]
        #If rsi is less than or equal to 30 buy
        if rsi[len(rsi) - 1] <= 30 and float(
                key['close_price']) <= currentSupport and not enteredTrade:
            print("Buying RSI is below 30!")
            #rh.place_buy_order(instrument, 1)
            enteredTrade = True
        #Sell when RSI reaches 70
        if rsi[len(rsi) - 1] >= 70 and float(
                key['close_price']
        ) >= currentResistance and currentResistance > 0 and enteredTrade:
            print("Selling RSI is above 70!")
            #rh.place_sell_order(instrument, 1)
            enteredTrade = False
        print("RSI: {}".format(rsi))
        print("SAM: {}".format(sma))
    #call this method again every 5 minutes for new price changes
    s.enter(300, 1, run, (sc, ))


s1.enter(1, 1, run, (s, ))
s1.run()