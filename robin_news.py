from pyrh import Robinhood
from datetime import datetime
from model.news import StockInfo
import config
import numpy as np
import tulipy as ti
import sched
import time
import pyotp
import json
import collections

totp = pyotp.TOTP(config.MFA).now()
rh = Robinhood()
rh.login(username=config.USERNAME,
         password=config.PASSWORD,
         qr_code=config.MFA)
#Initiate our scheduler so we can keep checking every minute for new price changes
s1 = sched.scheduler(time.time, time.sleep)


def fetch_news(sc1):
    print("Getting news\n")

    # incorporate discord

    # Have news be sent to "stock-news" channel in chat

    news = rh.get_news("WKHS")
    info_results = news["results"]
    for i in info_results:
        stock_info = StockInfo(i["title"], i["source"],
                               i["preview_text"].replace("\n\n", ""), i["url"])
        print(str(stock_info))

    s1.enter(300, 1, fetch_news, (sc1, ))


s1.enter(1, 1, fetch_news, (s1, ))
s1.run()