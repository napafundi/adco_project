from tkinter import *
import sqlite3
import modules
from tkinter import ttk
from PIL import Image, ImageTk

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

#create opening window tabs
notebook = ttk.Notebook(window, height = 650, width = 1024)
f1 = ttk.Frame(notebook)
f2 = ttk.Frame(notebook)
notebook.add(f1, text = "Raw Materials",padding=10)
notebook.add(f2, text = "Bottle Inventory",padding=10)
notebook.pack(padx=10, side = BOTTOM)

#create raw materials table
raw_materials = ttk.Treeview(f1, column = ("ID","Item","Amount"), show = "headings",height=600)
raw_materials.column("ID", anchor="center", width=250)
raw_materials.column("Item", anchor="center", width=250)
raw_materials.column("Amount", anchor="center", width=250)
raw_materials.heading("#1", text = "ID")
raw_materials.heading("#2", text="Date")
raw_materials.heading("#3", text="Amount")
raw_materials.pack(side=RIGHT,fill = Y)
modules.cur.execute("SELECT * FROM bottles")
rows = modules.cur.fetchall()
for row in rows:
    raw_materials.insert("",END,values = row)

#top-left raw materials frame
f4 = Frame(f1, height = 600,width=50)
f5 = LabelFrame(f4,height = 300, bd = 5, relief= RIDGE, text="View", font="bold")
b1 = Button(f5, text = "Bottles", width = 20)
b1.pack(anchor='center')
b2 = Button(f5, text = "Boxes", width = 20)
b2.pack(anchor='center')
b3 = Button(f5, text = "Caps", width = 20)
b3.pack(anchor='center')
b4 = Button(f5, text = "Capsules", width = 20)
b4.pack(anchor='center')
b5 = Button(f5, text = "Labels", width = 20)
b5.pack(anchor='center')
b6 = Button(f5, text = "All", width = 20)
b6.pack(anchor='center')

#mid-left production frame
f6 = LabelFrame(f4,height = 300, text = "Logistics", bd = 5, relief = RIDGE, font = "bold")
b7 = Button(f6, text="Production" , width = 20)
b7.pack(anchor='center')
b8 = Button(f6, text = "Raw Materials Received", width=20)
b8.pack(anchor='center')

f4.pack()
f5.pack()
f6.pack()





window.mainloop()
