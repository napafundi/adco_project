from tkinter import *
from datetime import datetime
from tkinter import ttk
import sqlite3
import openpyxl
import os
import string
import collections

table = 'pending_po'
cur_date = datetime.today().strftime('%Y-%m')
conn = sqlite3.Connection("inventory.db")
cur = conn.cursor()
cur.execute("SELECT product, amount, total " +
              "FROM " + table +
            " WHERE po_date " +
              "LIKE \'" + cur_date + "%\'")
pending_info = cur.fetchall()
cur.execute("SELECT product, price FROM bottles")
prod_prices = {key:val for (key, val) in cur.fetchall()}
conn.close()
pend_sale_total = sum([float(x[2][1:].replace(",", "")) for x in pending_info])
pend_sale_amts = {}
for (prod, amt) in [x[:2] for x in pending_info]:
    if prod in pend_sale_amts:
        pend_sale_amts[prod] += int(amt)
    else:
        pend_sale_amts[prod] = int(amt)
print(pending_info, prod_prices)
print(pend_sale_total)
print(pend_sale_amts)
sum = 0
for prod in pend_sale_amts.keys():
    sum += float(pend_sale_amts[prod] * prod_prices[prod])
print(sum)
