import sqlite3
from tkinter import *
import os
import webbrowser
import re

def database():
    global conn,cur
    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'raw materials' (id INTEGER PRIMARY KEY,item TEXT, amount INTEGER, price REAL, total REAL)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'production log' (id INTEGER PRIMARY KEY,product TEXT, amount INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'materials used' (id INTEGER PRIMARY KEY,product TEXT, amount INTEGER, date DATE)")
    cur.execute("CREATE TABLE IF NOT EXISTS bottles (id INTEGER PRIMARY KEY,item TEXT, amount INTEGER,price REAL, total REAL)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'grain inventory' (id INTEGER PRIMARY KEY,'order no.' TEXT, type TEXT, amount INTEGER,price REAL, total REAL)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'barrel inventory' (id INTEGER PRIMARY KEY,'barrel no.' TEXT, spirit TEXT,'proof gallons' INTEGER, 'date filled' DATE, age TEXT,investor TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'purchase orders' (date DATE,product TEXT, amount INTEGER, price REAL, total REAL, destination TEXT, 'PO no.' TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'employee transactions' (date DATE,product TEXT, amount INTEGER, employee TEXT)")
    conn.commit()

def add_item(table):
    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO bottles VALUES (NULL,?,?)",(item,amount,price,total))
    #cur.execute("INSERT INTO bottles VALUES (NULL,?,?)", ('',120))
    conn.commit()

def view_widget(window,widget,padx,location):
    for widg in window.pack_slaves():
        widg.pack_forget()

    widget.pack(padx=padx, side=location)

class Sheet_Label(Label):
    def __init__(self,master,text,file_location):

        Label.__init__(self,master,text=text,cursor="hand2",font="Times 14 underline",fg="#0000EE")
        def button_click(event):
            if self['fg'] =="#0000EE":
                self['fg'] = "#551A8B"
            else:
                self['fg'] = "#551A8B"
            file = webbrowser.open_new(file_location)
        self.bind("<Button-1>",func=button_click)

class Inventory_Button(Button):
    def __init__(self,master,text):

        Button.__init__(self,master,text=text,width=20,height=2)

def button_maker(list,master_widget):
    for item in list:
        button = Inventory_Button(master=master_widget,text=item)
        button.pack(anchor='center')

#used to search for the string literal within a filename that occurs before the
#file extension
fileRegex = re.compile(r'''
    ([a-zA-Z0-9_ -]+)
    (.)
    ([a-zA-Z_0-9])''',re.VERBOSE)
