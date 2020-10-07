
def update_trade_number(number_of_trades, filename):
    f = open(filename, "w")
    f.write(number_of_trades)
    f.close()


def get_number_of_trades(file):
    my_file = open(file, "r")
    content = my_file.read()
    number_of_trades = content
    my_file.close()
    return number_of_trades