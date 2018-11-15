from tkinter import *
import sqlite3
import modules
from tkinter import ttk

#home window information
window = Tk()
window.title("Albany Distilling Company Inventory")
width = 1024
height = 720
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
x = (screen_width/2) - (width/2)
y = (screen_height/2) - (height/2)
window.geometry("%dx%d+%d+%d" % (width,height,x,y))
window.resizable(0,0)

#create/load and display database
inventory = modules.database()
modules.display_database()

#create openeing window tabs
notebook = ttk.Notebook(window)
f1 = ttk.Frame(notebook)
f2 = ttk.Frame(notebook)
notebook.add(f1, text = "Raw Materials")
notebook.add(f2, text = "In Production")
notebook.grid()

#BALANCE TAB
b1 = Button(f1, text ="View Bottles").grid(padx="10",pady="5",row=0,column=0)
b2 = Button(f1, text="View Boxes").grid(padx="10",pady="5",row=1,column=0)

    #create balance table
tree = ttk.Treeview(f1, column = ("ID","Item","Amount"), show = "headings")
tree.column("ID", anchor="center")
tree.column("Item", anchor="center")
tree.column("Amount", anchor="center")
tree.heading("#1", text = "ID")
tree.heading("#2", text="Date")
tree.heading("#3", text="Amount")
tree.grid(row=0, column=2, rowspan=4)



window.mainloop()
