
def update_trade_number(number_of_trades, filename):
    original = open(filename, 'r')
    list_of_lines = []
    # Read file into a list
    for line, text in enumerate(original):
        if line == 0:
            text = "Number or day trades left: {}\n\nTransactions:\n\n".format(number_of_trades)
            list_of_lines.append(text)
        # First 4 lines
        elif line >= 3:
            list_of_lines.append(text)
    original.close()

    # Write list back to file
    modified = open(filename, 'w')
    [modified.write(str(lines)) for lines in list_of_lines]
    modified.close()

def get_number_of_trades(filename):
    my_file = open(filename, "r")
    content = my_file.readline()
    # Look for a digit in the first line of file
    content = [int(i) for i in content.split() if i.isdigit()]
    number_of_trades = content[0]
    my_file.close()
    return number_of_trades
