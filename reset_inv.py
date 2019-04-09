from tkinter import *
from datetime import datetime
from tkinter import ttk
import sqlite3
import openpyxl
import os
import string
import collections


conn = sqlite3.Connection("inventory.db")
cur = conn.cursor()
cur.execute("INSERT INTO 'estimated_cogs' VALUES (?,?,?,?,?,?,?,?,?)", (2.43, 2.12, 1.79, 1.27, 7.60, 2.02, 2.11, 4.4018, 35.49))
cur.execute("INSERT INTO 'estimated_cogs' VALUES (?,?,?,?,?,?,?,?,?)", (2.87, 1.70, 1.95, 1.30, 7.82, 2.02, 2.11, 4.7318, 39.04))
cur.execute("INSERT INTO barrel_count VALUES (?,?,?,?)", (0, 1, 300, 300))
conn.commit()
conn.close()
