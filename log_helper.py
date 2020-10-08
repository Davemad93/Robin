from datetime import datetime

def log_stock(stock, filename):
    f = open(filename, "a")
    f.write("\n{0} -- {1}".format(datetime.now().strftime("%Y-%m-%d %H:%M"), stock))
    f.close()

def read_file(file):
    my_file = open(file, "r")
    content = my_file.read()
    content_list = content.split("\n")
    my_file.close()
    clean_list =  []
    [clean_list.append(float(item.split(" -- ")[1])) for item in content_list]
    return clean_list

def print_portfolio_info(buying_power,shares_to_buy,latest_trading_price,estimated_trans_cost,rh,instrument,buyorsell):
    url = "https://api.robinhood.com/positions"
    pos_id = rh.instruments("SOLO")[0]['id']
    account = rh.positions()['results'][0]['account_number']
    url = "{}/{}/{}/".format(url, account, pos_id)
    for x in rh.positions()['results']:
        if x["url"] == url:
            average_buy_price = x['average_buy_price']
            shares_owned = float(x['quantity'])

    equity =  float(average_buy_price) * shares_owned
    print(equity)
    print(float(latest_trading_price) * int(shares_owned))
    gainsloses = round((float(latest_trading_price) * int(shares_owned)) - equity,2)

    # Buying
    if buyorsell == 1:
        return print("\nRSI is below 20 on the daily charts and we have enough money! \
                    \nAverage stock price: {} \
                    \nCurrent buying power: {} \
                    \nCurrent shares set to buy: {} \
                    \nCurrent trading price: {} \
                    \nCurrent number of shares owned: {} \
                    \nEstimated cost to buy: {} \
                    \nStart day trading!".format(average_buy_price,buying_power,shares_to_buy,latest_trading_price,shares_owned,round(estimated_trans_cost,2)))
    # Selling
    if buyorsell == 2:
        return print("\nRSI is above 80 on the daily charts! Let sell! \
                    \nAverage stock price: {} \
                    \nCurrent number of shares owned: {} \
                    \nCurrent trading price: {} \
                    \nEstimated gains/loses if selling all at curr trade price: {} \
                    \nStart day trading!".format(average_buy_price,shares_owned,latest_trading_price,gainsloses,))
