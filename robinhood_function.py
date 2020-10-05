from email.mime.text import MIMEText
from datetime import datetime
import smtplib
import config

def buy_stock(logic_data, entered_trade, close_prices, instrument, user, rh):
    # Check latest day:year rsi.
    rsi = logic_data['RSI']
    if rsi[-1] <= 30 and not entered_trade:  # and not enterTrade means we will not buy again after we bought in for this trade. This is typically for long positions, remove this for short pos
        msg = "RSI is below 20! Sending email that we are entering intraday trading to BUY our stock. Utilizing 5minute:day chart to do so"
        #send_email('ALERT!!!',msg)
        print(msg)

        rsi_5 = logic_data['RSI_5']
        print("Previous RSIs")
        for x in range(1, 11):
            print("CLOSE: {} RSI: {}".format(close_prices[-x], rsi_5[-x]))

        print("CURRENT RSI--", rsi_5[-1])
        # Check latest 5minute:60day rsi. If below 20 Buy!!
        if rsi_5[-1] <= 30 and user.num_of_trades > 0:
            # Market buy order, not a limit order.
            print("buying....")
            rh.place_buy_order(instrument, 10)
            user.bought_date = datetime.today()
            log_stock("bought at" + instrument,"database.txt")
            entered_trade = True # Entering trade

def log_stock(stock, filename):
    f = open(filename, "a")
    f.write("{0} -- {1}\n".format(datetime.now().strftime("%Y-%m-%d %H:%M"), stock))
    f.close()

def read_file(file):
    my_file = open(file, "r")
    content = my_file.read()
    content_list = content.split("\n")
    my_file.close()
    clean_list =  []
    [clean_list.append(float(item.split(" -- ")[1])) for item in content_list]
    return clean_list


def sell_stock(logic_data, entered_trade, close_prices, instrument, user, rh):
    # Check latest day:year rsi.
    rsi = logic_data['RSI']
    if rsi[-1] >= 80 and entered_trade: # Will only sell if we have entered a trade.
        msg = "RSI is abvove 80! Sending email that we are entering intraday trading to SELL our stock. Utilizing 5minute:day chart to do so"
        #send_email('ALERT!!!',msg)
        print(msg)

        rsi_5 = logic_data['RSI_5']
        print("Previous RSIs")
        for x in range(1, 11):
            print("CLOSE: {} RSI: {}".format(close_prices[-x], rsi_5[-x]))

        # Check latest 5minute:60day rsi. If above 80 SELL!!
        if rsi_5[-1] >= 80 and user.num_of_trades > 0:
            # Market buy order, not a limit order.
            print("selling....")
            rh.place_sell_order(instrument, 10)
            entered_trade = False # Exiting trade
            log_stock("sold at" + instrument,"database.txt")
            if user.bought_date == datetime.today:
                user.num_of_trades -= 1

def send_email(sbj, msg):
    gmail_user = config.GUSER 
    gmail_password = config.GPASS
    text_type = 'plain'
    text = msg
    msg = MIMEText(text, 'plain', 'utf-8') # plain/html
    msg['Subject'] = sbj
    msg['From'] = gmail_user
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.login(gmail_user, gmail_password)
    for email in config.EMAILS:
        server.sendmail(msg['From'], email, msg.as_string())
    server.quit()
            

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