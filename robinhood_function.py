from datetime import datetime
import log_helper
import email_client
import database_function

database = "database.txt"


def buy_stock(logic_data, instrument, user, rh):
    rsi = logic_data['RSI']
    # Check latest day:year rsi.
    if rsi[-1] <= 20:
        print("Daily RSI is below 20.")
        print(user)
        if user.buying_power > user.estimated_trans_cost:
            rsi_5 = logic_data['RSI_5']
            print("\nCURRENT FIVE MIN RSI--", rsi_5[-1])

            # Check latest 5minute:60day rsi. If below 20 Buy
            if rsi_5[-1] <= 20 and user.day_trades > 0:
                print("5 minute RSI below 20. Buying....\n")
                #rh.place_buy_order(instrument, 1)

                user.bought_date = datetime.today()
                # TODO: Need an avg cost func made
                log_helper.log_stock("Bought at: $" + user.get_latest_trading_price, database)

        elif buying_power < estimated_trans_cost:
            print("Warning youre trying to buy more than you have money for.")


def sell_stock(logic_data, instrument, user, rh):
    rsi = logic_data['RSI']
    # Check latest day:year rsi.
    if rsi[-1] >= 80:
        print("Daily RSI is above 80.")
        print(user)
        if user.day_trades > 0: # TODO: and has an open position.
            rsi_5 = logic_data['RSI_5']
            print("\nCURRENT FIVE MIN RSI--", rsi_5[-1])
            #email_client.send_email('ALERT!!!',msg)
            
            # Check latest 5minute:60day rsi. If above 80 SELL
            if logic_data["RSI_5"][-1] >= 80:
                print("5 minute RSi is above 80. Selling....\n")
                #rh.place_sell_order(instrument, 1)

                log_helper.log_stock("Sold at: $" + user.get_latest_trading_price, database)
                # TODO: (sp - avgcost) * shares = profits gained/lost ....I think.
                if user.bought_date == datetime.today:
                    user.day_trades -= 1
                    database_function.update_trade_number(str(user.day_trades), database)
                    print("\nONLY "+ user.day_trades + " LEFT!")
        else:
            print("OUT OF DAY TRADES OR DONT HAVE AN OPEN POSITION")

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

