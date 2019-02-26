import os

try:
    yeet = os.listdir(os.getcwd() + "\\purchase_orders\\" + str(2019))
    new_po_num = str(2020) + "-" + '{:03}'.format(1)
    print(yeet)
except FileNotFoundError:
    os.mkdir(os.getcwd() + "\\purchase_orders\\" + str(2020))
