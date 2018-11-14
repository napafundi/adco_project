from tkinter import *
import sqlite3
import databases
from tkinter import ttk

window = Tk()
window.title("Albany Distilling Company Inventory")
bottles_db = databases.Bottle_Database("bottle_inventory.db")

#FUNCTIONS

    #update balance


#create window tabs
notebook = ttk.Notebook(window)
f1 = ttk.Frame(notebook)
f2 = ttk.Frame(notebook)
notebook.add(f1, text = "Bottle Inventory")
notebook.add(f2, text = "Grain Inventory")
notebook.grid()


#BALANCE TAB
l1 = Label(f1, text="Item").grid(row=0,column=0)
e1 = Entry(f1, text="").grid(padx="10",row=0,column=1)
l2=Label(f1, text="Amount").grid(row=1,column=0)
e2 = Entry(f1, text="").grid(padx="10",row=1,column=1)
b1 = Button(f1, text ="Update Amount").grid(padx="10",pady="10",row=2,column=0)

    #create balance table
tree = ttk.Treeview(f1, column = ("ID","Item","Amount"), show = "headings")
tree.column("ID", anchor="center")
tree.column("Item", anchor="center")
tree.column("Amount", anchor="center")
tree.heading("#1", text = "ID")
tree.heading("#2", text="Date")
tree.heading("#3", text="Amount")
tree.grid(row=0, column=2, rowspan=4)


bottles_db.view()
for row in bottles_db.rows:
    tree.insert("",END,values = row)

#TRANSACTION TAB

    #create transactions table
tree_2 = ttk.Treeview(f2, column = ("Date","Amount","Location","Type"), show = "headings")
tree_2.column("Date", anchor="center")
tree_2.column("Amount", anchor="center" )
tree_2.column("Location", anchor="center")
tree_2.column("Type", anchor="center")
tree_2.heading("#1", text="Date")
tree_2.heading("#2", text="Amount")
tree_2.heading("#3", text="Location")
tree_2.heading("#4", text="Type")
tree_2.grid()



window.mainloop()
