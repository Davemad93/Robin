from email.mime.text import MIMEText
from datetime import datetime
import smtplib
import config

def buy_stock(logic_data, instrument, user, rh, quote_data):
    # Check latest day:year rsi.
    rsi = logic_data['RSI']
    print("CURRENT DAILY RSI--", rsi[-1])
    if rsi[-1] <= 45 and  user.num_of_trades < 4: # TODO: Figure out day trading limit logic
        msg = "\nRSI is below 30 on the daily charts! Start day trading!"
        #send_email('ALERT!!!',msg)
        print(msg)

        rsi_5 = logic_data['RSI_5']

        print("\nCURRENT FIVE MIN RSI--", rsi_5[-1])
        # Check latest 5minute:60day rsi. If below 20 Buy!!
        if rsi_5[-1] <= 65 and user.num_of_trades > 0:
            print("Buying....\n")
            #rh.place_buy_order(instrument, 1)
            user.bought_date = datetime.today()
            log_stock("Bought at: $" + logic_data["LTP"] + " Making your avg cost to be...","database.txt") # TODO: Need an avg cost func made
            user.num_of_trades += 1

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


def sell_stock(logic_data, instrument, user, rh, quote_data):
    # Check latest day:year rsi.
    rsi = logic_data['RSI']
    if rsi[-1] >= 80 and user.num_of_trades > 0: # TODO: Figure out day trading limit logic
        msg = "\nRSI is abvove 80 on the daily charts! Start day trading!"
        #send_email('ALERT!!!',msg)
        print(msg)

        print("\nCURRENT FIVE MIN RSI--", rsi_5[-1])
        # Check latest 5minute:60day rsi. If above 80 SELL!!
        if logic_data["RSI_5"][-1] >= 80:
            print("Selling....\n")
            #rh.place_sell_order(instrument, 1)
            log_stock("Sold at: $" + logic_data["LTP"] + " With a profit of...", "database.txt") # TODO: (sp - avgcost) * shares = profits gained/lost ....I think.
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
