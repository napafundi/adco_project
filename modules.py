import sqlite3
from tkinter import *
import os
import webbrowser
import re
from tkinter import messagebox

def database():
    global conn,cur
    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'raw materials' (type TEXT,item TEXT, amount INTEGER, price REAL, total REAL)")
    cur.execute("UPDATE 'raw materials' SET 'total'= PRINTF('%s%g', '$', amount*price)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'production log' (product TEXT, amount INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'bottles' (type TEXT, product TEXT, amount INTEGER,price REAL, total REAL)")
    cur.execute("UPDATE 'bottles' SET 'total'= PRINTF('%s%g', '$', amount*price)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'grain inventory' ('order no.' TEXT, type TEXT, amount INTEGER,price REAL, total REAL)")
    cur.execute("UPDATE 'grain inventory' SET 'total'= PRINTF('%s%g', '$', amount*price)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'barrel inventory' ('barrel no.' TEXT, type TEXT,'proof gallons' INTEGER, 'date filled' DATE, age TEXT,investor TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'purchase orders' (date DATE,product TEXT, amount INTEGER, price REAL, total REAL, destination TEXT, 'PO no.' TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'employee transactions' (date DATE,product TEXT, amount INTEGER, employee TEXT)")
    conn.commit()
    conn.close()

def add_item(sqlite_table,toplevel_widg):
    '''Work through toplevel to find entry widgets and extract these values to be
    inserted into the given sqlite_table.

    Parameters:
    sqlite_table (str):The name of the sqlite table to add items to.
    toplevel_widg (Tk toplevel object):The toplevel widget object to be worked through.
    '''

    additions = []
    num_entries = 0
    for entry in filter(lambda x: x.winfo_class() == 'Entry',reversed(toplevel_widg.grid_slaves())): #work through add_item entry widgets
        if entry.get():
            additions.append(entry.get())
            num_entries += 1
        else:
            messagebox.showerror("Input Error","At least one input is blank, please try again.")
            return
    additions = tuple(additions)
    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO \'" + sqlite_table + "\' VALUES (" + ("?,"*(num_entries-1)) + "?)", additions)
    conn.commit()
    conn.close()
    toplevel_widg.destroy()

def view_widget(window,widget,padx,location):
    '''Removes current packed widgets from window frame and replaces with new widget
    chosen.

    Parameters:
    window (Tk root object):Master window to remove widgets from
    widget (Tk widget object):Widget to be displayed
    padx (int):Widget x-padding value
    location (str):Position to place new widget
    '''

    for widg in window.pack_slaves():
        widg.pack_forget()
    widget.pack(padx=padx, side=location)

def view_products(sqlite_table,column,item,gui_table):
    '''Fetches info from sqlite_table based on an item filter. Returns information
    into the current gui_table.

    Parameters:
    sqlite_table(str):Sqlite table to fetch data from.
    column (str):Column to which the 'item' filter is applied.
    item (str):Item which is filtered for.
    gui_table (Tk treeview object):Table where info will be displayed.
    '''

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
    '''Creates a clickable label with link to file in given file location.

    Parameters:
    master (Tk widget object):Tkinter widget to place label button within.
    text (str):Text value to be displayed for the label.
    file_location (str):Directory containing the file to be linked.
    '''

    def __init__(self,master,text,file_location):

        Label.__init__(self,master,text=text,cursor="hand2",font="Times 14 underline",fg="#0000EE")
        def button_click(event):
            '''Changes label color from 'blue' to 'purple' and opens the file.'''
            if self['fg'] =="#0000EE":
                self['fg'] = "#551A8B"
            else:
                self['fg'] = "#551A8B"
            file = webbrowser.open_new(file_location)
        self.bind("<Button-1>",func=button_click)

#gives view button functionality to view items by type
class View_Button(Button):
    def __init__(self,master,text,sqlite_table,gui_table):
        self.sqlite_table = sqlite_table
        self.gui_table = gui_table
        Button.__init__(self,master,text=text,command = lambda: view_products(sqlite_table,"Type",text,gui_table),width=20,height=2)

#gives production buttons functionality
class Inventory_Button(Button):
    def __init__(self,master,text,sqlite_table,gui_table):
        self.sqlite_table = sqlite_table
        self.gui_table = gui_table
        Button.__init__(self,master,text=text,width=20,height=2)

#iterates through list of items and creates buttons based on 'class_name' object
def button_maker(class_name,list,master_widget,sqlite_table,gui_table):
    for item in list:
        button = class_name(master=master_widget,text=item,sqlite_table=sqlite_table,gui_table=gui_table)
        button.pack(anchor='center')

#used to search for the string literal within a filename that occurs before the file extension (Ex. '.txt')
fileRegex = re.compile(r'''
    ([a-zA-Z0-9_ -]+)
    (.)
    ([a-zA-Z_0-9])''',re.VERBOSE)
