from pyrh import Robinhood
from datetime import datetime
from email.mime.text import MIMEText
import config
import numpy as np
import tulipy as ti
import yahoo_finance
import sched, time
import pyotp
import smtplib

#A Simple Robinhood Python Trading Bot using RSI (buy <=30 and sell >=70 RSI) and with support and resistance.
#totp = pyotp.TOTP("").now()
#print(totp)

# Log in to Robinhood app (will prompt for two-factor)
rh = Robinhood()
rh.login(username=config.USERNAME,
         password=config.PASSWORD,
         qr_code=config.MFA)

#Setup our variables, we haven't entered a trade yet and our RSI period
entered_trade = False
day_period = 251

#Initiate our scheduler so we can keep checking every minute for new price changes
s = sched.scheduler(time.time, time.sleep)


def run(sc):
    global entered_trade
    global day_period
    time_string = time.strftime("%m/%d/%Y, %H:%M:%S", time.localtime())

    print("Getting historical quotes on {}".format(time_string))
    stock_ticker = "WKHS"
    day_year_quotes = rh.get_historical_quotes(stock_ticker, 'day', 'year')  # Currently getting years worth of data by day. 251 days worth.

    fivemin_day_quotes = rh.get_historical_quotes(stock_ticker, '5minute', 'day')  # this only gets the current dats 5min data

    five_min_day_yahoo = yahoo_finance.get_stock_history("WKHS","1d","5m") # This gets the last 60 days including today.

    close_prices = []
    fivemin_close_prices = []
    # Get all closing prices.
    for key in day_year_quotes["results"][0]["historicals"]:
        close_prices.append(float(key['close_price']))

    for key in fivemin_day_quotes["results"][0][
            "historicals"]:  # Data starts at 13:30 - 19:55 AKA 8:30am - 2:55pm
        fivemin_close_prices.append(float(key['close_price']))

    #print(* fivemin_day_quotes["results"][0]["historicals"], sep='\n')

    # Data before manual price add.
    DATA = np.array(close_prices)
    FIVEMIN_DATA = np.array(five_min_day_yahoo)

    # adds latest trading price to the list of day:year closing prices. Not sure how this will affect indicators.
    close_prices.append(float(rh.quote_data("WKHS")['last_trade_price']))
    EXP_DATA = np.array(close_prices)  # Data with latest trading price

    #Calculate Indicators and get instrument we will be trading.
    indicator_period = 3
    rsi = ti.rsi(DATA, period=indicator_period)  # Currently only using this one

    stochrsi = ti.stochrsi(DATA, period=indicator_period)
    current_rsi = ti.rsi(EXP_DATA, period=indicator_period)
    #sma = ti.sma(DATA, period=indicator_period)
    #ema = ti.ema(DATA, period=indicator_period)

    instrument = rh.instruments(stock_ticker)[0]

    # Extra variables that are not being used. Just saving.
    # yesterdays close price
    previous_close_price = rh.previous_close(stock_ticker)
    # last trade price i think is 8pm\7:55pm
    last_trade_price = rh.last_trade_price(stock_ticker)
    last_extended_hours_price = rh.get_quote(stock_ticker)['last_extended_hours_trade_price']

    five_recent_rsi = {}
    rsi[-1] = 17  ## TEST TO GET INTO STATEMENT!!

    ## BUYING LOGIC - If rsi is less than or equal to 20 move to next stage
    buy_stock(rsi, entered_trade, fivemin_day_quotes, FIVEMIN_DATA)

    ## SELLING LOGIG - if rsi is greater than or equal to 80 move to next stage
    sell_stock(rsi, entered_trade, day_year_quotes)

    #call this method again every 5 minutes for new price changes
    s.enter(300, 1, run, (sc, ))


def buy_stock(rsi, entered_trade, fivemin_day_quotes, type_of_data):
    if rsi[-1] <= 20 and not entered_trade:  # and not enterTrade means we will not buy again after we bought in for this trade. This is typically for long positions, remove this for short pos
        msg = "RSI is above 80! Send signal that it may be time to sell / move into next stage and find a nice price to sell at. Utilize 5minute:day chart to do so"
        #send_email('ALERT!!!',msg)
        print(msg)

        #if (len(fivemin_close_prices) >= (indicator_period)): # May need this for when the day starts if we cant get previous days 5 min data.
        # Start 5 min chart data area
        indicator_period = 5
        fivemin_rsi = ti.rsi(type_of_data, period=indicator_period)  # Cant get correct numbers, comparing with tradeview

        fivemin_stochrsi = ti.stochrsi(type_of_data, period=indicator_period)  # Cant get correct numbers, comparing with tradeview

        print("Previous RSIs")
        for x in range(1, 11):
            date = fivemin_day_quotes["results"][0]["historicals"][-x]['begins_at']
            print("Date: {} RSI: {}".format(date, fivemin_rsi[-x]))
            print("Date: {} CLOSE: {}".format(date, type_of_data[-x]))

        # Market buy order, not a limit order.
        #rh.place_buy_order(instrument, 10)
        entered_trade = True


def sell_stock(rsi, entered_trade, day_year_quotes):
    if rsi[-1] >= 80 and entered_trade:
        print("RSI is above 80! Send signal that it may be time to sell / move into next stage and find a nice price to sell at. Utilize 5minute:day chart to do so")

        print("Previous 5 RSIs")
        for x in range(1, 6):
            date = day_year_quotes["results"][0]["historicals"][-x][
                'begins_at']
            print("Date: {} RSI: {}".format(date, rsi[-x]))

        # Market buy order, not a limit order.
        #rh.place_sell_order(instrument, 10)
        entered_trade = False


# takes in two numbers and gives back the percent difference wheather it be an increase or decrease.
def calculate_percent_difference(prev_num, curr_num):
    if curr_num > prev_num:  # This is a percent increase
        increase = float(curr_num) - float(prev_num)
        percent_increase = (increase / float(prev_num)) * 100
        return "The percent increase is: {}".format(percent_increase)  # if number is negative then this is a percent decrease
    elif curr_num < prev_num:
        decrease = float(prev_num) - float(curr_num)
        percent_decrease = (decrease / float(prev_num)) * 100
        return "The percent decrease is: {}".format(percent_decrease)  # if answer is negative then this is a percent increase
    elif curr_num == prev_num:
        return "curr_num and prev_num are equal."
    else:
        return "Some error occured, mayday!!!!"

def send_email(sbj, msg):
    gmail_user = 'xtraderbotx@gmail.com'
    gmail_password = '9&y6GPWrA!pnu9M9u4iv'
    text_type = 'plain'
    text = msg
    msg = MIMEText(text, 'plain', 'utf-8') # plain/html
    msg['Subject'] = sbj
    msg['From'] = 'xtraderbotx@gmail.com'
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(gmail_user, gmail_password)
    for email in config.EMAILS:
        server.sendmail(msg['From'], email, msg.as_string())
        #server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


s.enter(1, 1, run, (s, ))
s.run()


if __name__ == '__main__':
    run()
