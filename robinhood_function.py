from datetime import datetime
import log_helper
import email_client


def buy_stock(logic_data, instrument, user, rh, quote_data):
    # Check latest day:year rsi.
    rsi = logic_data['RSI']
    print("\nCURRENT DAILY RSI--", rsi[-1])
    if rsi[-1] <= 20 and  user.num_of_trades > 0:
        print("\nRSI is below 20 on the daily charts! Start day trading!")
        #email_client.send_email('ALERT!!!',msg)

        rsi_5 = logic_data['RSI_5']

        print("\nCURRENT FIVE MIN RSI--", rsi_5[-1])
        # Check latest 5minute:60day rsi. If below 20 Buy!!
        if rsi_5[-1] <= 20 and user.num_of_trades > 0:
            print("Buying....\n")
            #rh.place_buy_order(instrument, 1)

            user.bought_date = datetime.today()
            # TODO: Need an avg cost func made
            log_helper.log_stock("Bought at: $" + logic_data["LTP"] + " Making your avg cost to be...","database.txt")

def sell_stock(logic_data, instrument, user, rh, quote_data):
    # Check latest day:year rsi.
    rsi = logic_data['RSI']
    if rsi[-1] >= 80 and user.num_of_trades > 0:
        print("\nRSI is abvove 80 on the daily charts! Start day trading!")
        #email_client.send_email('ALERT!!!',msg)
        
        rsi_5 = logic_data['RSI_5']
        print("\nCURRENT FIVE MIN RSI--", rsi_5[-1])
        # Check latest 5minute:60day rsi. If above 80 SELL!!
        if logic_data["RSI_5"][-1] >= 80:
            print("Selling....\n")
            #rh.place_sell_order(instrument, 1)

            # TODO: (sp - avgcost) * shares = profits gained/lost ....I think.
            log_helper.log_stock("Sold at: $" + logic_data["LTP"] + " With a profit of...", "database.txt")
            if user.bought_date == datetime.today:
                user.num_of_trades -= 1
                print("\nONLY "+ user.num_of_trades + "LEFT!")          

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
