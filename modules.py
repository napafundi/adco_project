import sqlite3
from tkinter import *
import os
import webbrowser
import re

def database():
    global conn,cur
    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'raw materials' (id INTEGER PRIMARY KEY,type TEXT,item TEXT, amount INTEGER, price REAL, total REAL)")
    cur.execute("UPDATE 'raw materials' SET 'total'= PRINTF('%s%g', '$', amount*price)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'production log' (id INTEGER PRIMARY KEY,product TEXT, amount INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'bottles' (id INTEGER PRIMARY KEY,type TEXT, item TEXT, amount INTEGER,price REAL, total REAL)")
    cur.execute("UPDATE 'bottles' SET 'total'= PRINTF('%s%g', '$', amount*price)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'grain inventory' (id INTEGER PRIMARY KEY,'order no.' TEXT, type TEXT, amount INTEGER,price REAL, total REAL)")
    cur.execute("UPDATE 'grain inventory' SET 'total'= PRINTF('%s%g', '$', amount*price)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'barrel inventory' (id INTEGER PRIMARY KEY,'barrel no.' TEXT, type TEXT,'proof gallons' INTEGER, 'date filled' DATE, age TEXT,investor TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'purchase orders' (date DATE,product TEXT, amount INTEGER, price REAL, total REAL, destination TEXT, 'PO no.' TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'employee transactions' (date DATE,product TEXT, amount INTEGER, employee TEXT)")
    conn.commit()

def add_item():
    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO 'bottles' VALUES (NULL,?,?,?,?,?)",("Vodka","Vodka","43","12.15","32"))
    cur.execute("INSERT INTO 'raw materials' VALUES (NULL,?,?,?,?,?)",("Caps","red","24","32","12.27"))
    conn.commit()

def view_widget(window,widget,padx,location):
    for widg in window.pack_slaves():
        widg.pack_forget()

    widget.pack(padx=padx, side=location)

def view_products(sqlite_table,column,item,gui_table):
    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    if item == "All":
        cur.execute("SELECT * FROM \'" + sqlite_table + "\'")
    else:
        cur.execute("SELECT * FROM \'" + sqlite_table + "\' WHERE " + column + "= \'" + item + "\'")
    rows = cur.fetchall()
    for item in gui_table.get_children():
        gui_table.delete(item)
    for row in rows:
        gui_table.insert("",END,values = row)

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

class View_Button(Button):
    def __init__(self,master,text,sqlite_table,gui_table):
        self.sqlite_table = sqlite_table
        self.gui_table = gui_table
        Button.__init__(self,master,text=text,command = lambda: view_products(sqlite_table,"Type",text,gui_table),width=20,height=2)

class Inventory_Button(Button):
    def __init__(self,master,text,sqlite_table,gui_table):
        self.sqlite_table = sqlite_table
        self.gui_table = gui_table
        Button.__init__(self,master,text=text,width=20,height=2)

def button_maker(class_name,list,master_widget,sqlite_table,gui_table):
    for item in list:
        button = class_name(master=master_widget,text=item,sqlite_table=sqlite_table,gui_table=gui_table)
        button.pack(anchor='center')

#used to search for the string literal within a filename that occurs before the
#file extension
fileRegex = re.compile(r'''
    ([a-zA-Z0-9_ -]+)
    (.)
    ([a-zA-Z_0-9])''',re.VERBOSE)
