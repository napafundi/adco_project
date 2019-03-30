from tkinter import *
from datetime import datetime
from tkinter import ttk
import sqlite3

def monthly_reports_update():
    totals_tables = ['raw_materials', 'bottles', 'samples', 'grain',
                     'purchase_orders']
    monthly_totals = {}
    conn = sqlite3.Connection("inventory.db")
    conn.row_factory = lambda cursor, row: row[0]
    cur = conn.cursor()
    for table in totals_tables:
        cur.execute("SELECT total " +
                      "FROM " + table)
        total = sum([float(x[1:].replace(",","")) for x in cur.fetchall()])
        monthly_totals[table] = total
    print(monthly_totals)

monthly_reports_update()
