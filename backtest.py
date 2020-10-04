#####################################################
### Uses given trading strategy to log buys and sells
### and generate gains and losses info and more.
### 
### Current Strategy: Red, white, blue.
### - uses 6 short and long term emas and buys/sells
### when the min of the short term and max of the 
### long term cross.
#####################################################
import pandas as pd
import numpy as np
import yfinance as yf
import datetime as dt
from pandas_datareader import data as pdr

yf.pdr_override()

stock = input("Enter a stock a ticker symbol: ").upper()
print(stock)

start = dt.datetime(2019, 1, 1) # Year, Month, Day

now = dt.datetime.now()

df = pdr.get_data_yahoo(stock, start, now)

emas_used = [3,5,8,10,12,15,30,35,40,45,50,60]
for x in emas_used:
    ema = x
    df["Ema_" + str(ema)] = round(df.iloc[:,4].ewm(span=ema, adjust=False).mean(),2)
print(df.tail())

pos = 0 # 1 is entered 0 = not entered position
num = 0 # row we are on
percent_change = [] # result of trades

for i in df.index:
    # minimum of the short term emas
    cmin = min(df["Ema_3"][i],df["Ema_5"][i],df["Ema_8"][i],df["Ema_10"][i],df["Ema_12"][i],df["Ema_15"][i])
    # maximum of the long term emas
    cmax = max(df["Ema_30"][i],df["Ema_35"][i],df["Ema_40"][i],df["Ema_45"][i],df["Ema_50"][i],df["Ema_60"][i])

    close = df["Adj Close"][i]
    shares = 1 # Numbers of shares to trade
    if(cmin>cmax): # buy condition
        print("Red White Blue")
        if(pos==0):
            bp = close * shares # adj close price * shares
            pos = 1
            print("Buying now at "+str(bp))

    elif(cmin<cmax): # Sell condition
        print("Blue White Red")
        if (pos==1):
            pos = 0
            sp = close * shares # adj close price * shares
            print("Selling now at "+str(sp))
            pc = (sp/bp-1)*100 # Percent change
            percent_change.append(pc)

    # if we are at the end of the pandas dataframe and we still have a pos open
    if(num==df["Adj Close"].count()-1 and pos==1):
        pos = 0
        sp = close
        print("Selling now at "+str(pc))
        pc = (sp/bp-1)*100
        percent_change.append(pc)

    num=+1

print(percent_change)

gains = 0
ng = 0      # number/total of gains
losses = 0
nl = 0      # number.total of losses
totalR = 1  # Total return, starting at 1

for i in percent_change:
    # If winning trade
    if(i>0):
        gains+=i
        ng+=1
    # If lossing trade
    else:
        losses+=i
        nl+=1
    totalR = totalR*((i/100)+1) # 

# multiplies all diff percentages together and gets total return if you were going all in or out.
totalR = round((totalR-1)*100,2)

# Max and Avg gains
if(ng>0):
    avg_gain = gains/ng
    maxR = str(max(percent_change))
else:
    avg_gain = 0
    maxR = "undefined"

# Min and Avg losses
if(nl>0):
    avg_loss = losses/nl
    maxL = str(min(percent_change))
    ratio = str(-avg_gain/avg_loss) # risk reward relationship
else:
    avg_loss = 0
    maxL = "undefined"
    ratio = "inf"

# Perentage of time where a trade ended up with a gain
if (ng>0 or nl>0):
    batting_avg = ng/(ng+nl) # use nl/(ng+nl) to get percentage of losses
else:
    batting_avg = 0

print()
print("Results for "+ stock +" going back to "+str(df.index[0])+", Sample size: "+str(ng+nl)+" trades")
print("EMAs used: "+str(emas_used))
print("Batting Avg: "+ str(batting_avg))
print("Gain/loss ratio: "+ ratio)
print("Average Gain: "+ str(avg_gain))
print("Average Loss: "+ str(avg_loss))
print("Max Return: "+ maxR)
print("Max Loss: "+ maxL)
print("Total return over "+str(ng+nl)+ " trades: "+ str(totalR)+"%" )
print()
