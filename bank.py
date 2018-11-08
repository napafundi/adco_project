from tkinter import *
import sqlite3
import backend
from tkinter import ttk

window = Tk()
window.title("Bank Account")
balance_db = backend.Balance_Database("balance.db")
transaction_db = backend.Transaction_Database("transactions.db")

#button commands
def balance():
    balance_db.view()
    for row in balance_db.rows:
        tree.insert("",END,values = row)

def transactions():
    transaction_db.view()
    for row in transaction_db.rows:
        tree_2.insert("",END,values = row)



#create tabs
notebook = ttk.Notebook(window)
f1 = ttk.Frame(notebook)
f2 = ttk.Frame(notebook)
notebook.add(f1, text = "Balance")
notebook.add(f2, text = "Transactions")
notebook.pack(expand=1, fill="both")



#create balance table
tree = ttk.Treeview(f1, column = ("Date","Amount"), show = "headings")
tree.column("Date", anchor="center")
tree.column("Amount", anchor="center")
tree.heading("#1", text="Date")
tree.heading("#2", text="Amount")
tree.pack(fill = "both", expand = True)

#create a transactions table
tree_2 = ttk.Treeview(f2, column = ("Date","Amount","Location","Type"), show = "headings")
tree_2.column("Date", anchor="center")
tree_2.column("Amount", anchor="center" )
tree_2.column("Location", anchor="center")
tree_2.column("Type", anchor="center")
tree_2.heading("#1", text="Date")
tree_2.heading("#2", text="Amount")
tree_2.heading("#3", text="Location")
tree_2.heading("#4", text="Type")
tree_2.pack(fill = "both", expand = True)



#display the application
#transaction_db.change_balance("11/5/2018",35.00, "Target", "Food")
#transaction_db.view()

balance()
transactions()
window.mainloop()
