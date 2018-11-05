from tkinter import *
import sqlite3
import backend
from tkinter import ttk

window = Tk()
window.title("Bank Account")
database = backend.Database()

#button commands
def balance():
    database.view()
    for row in database.rows:
        tree.insert("",END,values = row)

#create tabs
notebook = ttk.Notebook(window)
f1 = ttk.Frame(notebook)
f2 = ttk.Frame(notebook)
notebook.add(f1, text = "Balance")
notebook.add(f2, text = "Transactions")
notebook.pack(expand=1, fill="both")

#create balance table
tree = ttk.Treeview(window, column = ("Date","Amount"), show = "headings")
tree.heading("#1", text = "Date")
tree.heading("#2", text = "Amount")
tree.pack()


#display the application
#database.change_balance(r"11/20/2018", 30.00)
balance()
window.mainloop()
