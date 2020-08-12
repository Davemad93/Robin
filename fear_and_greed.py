import robin_stocks as rh
import requests
from bs4 import BeautifulSoup


def fear_and_greed():
    FEAR_AND_GREED_URL = "https://money.cnn.com/data/fear-and-greed/"
    FEAR_AND_GREED_NOW = "Fear &amp; Greed Now: "
    FEAR_AND_GREED_PREV = "Fear &amp; Greed Previous Close: "
    FEAR_AND_GREED_WEEK = "Fear &amp; Greed 1 Week Ago: "
    FEAR_AND_GREED_MONTH = "Fear &amp; Greed 1 Month Ago: "
    FEAR_AND_GREED_YEAR = "Fear &amp; Greed 1 Year Ago: "
    LAST_UPDATE = "Last updated "
    FEAR_THRESHOLD = 15
    GREED_THRESHOLD = 80
    history={}

    r = requests.get(FEAR_AND_GREED_URL)

    html = r.content

    soup = BeautifulSoup(html)

    div = soup.find_all(id='needleChart')
    

    # Get last updated date
    position = str(soup.find_all(id='needleAsOfDate')[0]).find("Last Updated ")
    position = position + len("Last Updated ")
    last_update = str(soup.find_all(id='needleAsOfDate')[0])[25:53]
    print(last_update)

    div = str(div[0])


    # Get Current S&P500 fear and greed index as of last updated date
    position = div.find(FEAR_AND_GREED_NOW)
    position = position + len(FEAR_AND_GREED_NOW)
    current_index = int(div[position:position+3].strip())

    # Get previous close index   
    position = div.find(FEAR_AND_GREED_PREV)
    position = position + len(FEAR_AND_GREED_PREV)
    prev_close_index = int(div[position:position+3].strip())

    # Get 1 week ago index   
    position = div.find(FEAR_AND_GREED_WEEK)
    position = position + len(FEAR_AND_GREED_WEEK)
    week_ago_index = int(div[position:position+3].strip())

    # Get 1 month ago index   
    position = div.find(FEAR_AND_GREED_MONTH)
    position = position + len(FEAR_AND_GREED_MONTH)
    month_ago_index = int(div[position:position+3].strip())

   # Get 1 year ago index   
    position = div.find(FEAR_AND_GREED_YEAR)
    position = position + len(FEAR_AND_GREED_YEAR)
    year_ago_index = int(div[position:position+3].strip())


    print("Current Index: {}".format(current_index))
    print("Previous Close Index: {}".format(prev_close_index))
    print("1 Week Ago Index: {}".format(week_ago_index))
    print("1 Month Ago Index: {}".format(month_ago_index))
    print("1 Year Ago Index: {}".format(year_ago_index))
    history[last_update] = {"current_index":current_index,
                            "previous_index":prev_close_index,
                            "week_index":week_ago_index,
                            "month_index":month_ago_index,
                            "year_index":year_ago_index}
    print(history)

    

    #print(current_fear_and_greed_index)
    #print(type(current_fear_and_greed_index))
    

def main():
    print("Starting Fear and Greed Program")
    fear_and_greed()


if __name__ == '__main__':
    main()
