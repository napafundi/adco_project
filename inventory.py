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

#create opening window tabs
notebook = ttk.Notebook(window, height = 600, width = 800)
f1 = ttk.Frame(notebook)
f2 = ttk.Frame(notebook)
f3 = ttk.Frame(notebook)
notebook.add(f1, text = "Raw Materials",padding=10)
notebook.add(f2, text = "In Production",padding=10)
notebook.add(f3, text = "Bottle Inventory",padding=10)
notebook.pack(side = RIGHT, padx=10)

#create raw materials table
raw_materials = ttk.Treeview(f1, column = ("ID","Item","Amount"), show = "headings",height=600)
raw_materials.column("ID", anchor="center")
raw_materials.column("Item", anchor="center")
raw_materials.column("Amount", anchor="center")
raw_materials.heading("#1", text = "ID")
raw_materials.heading("#2", text="Date")
raw_materials.heading("#3", text="Amount")
raw_materials.pack(fill = BOTH)

#buttons widget
f4 = Frame(window, height = 600)
b1 = Button(f4, text = "View Bottles")
b1.pack(anchor='center', padx=30,pady=10)
b2 = Button(f4, text = "View Boxes")
b2.pack(anchor='center', padx=30, pady=10)
f4.pack(side=LEFT)




window.mainloop()
