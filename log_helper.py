from datetime import datetime

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