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

#MAIN MENU/BOTTLE INV
notebook = ttk.Notebook(window, height = 650, width = 1024)
raw_frame = ttk.Frame(notebook)
bottle_frame = ttk.Frame(notebook)
notebook.add(raw_frame, text = "Raw Materials",padding=10)
notebook.add(bottle_frame, text = "Bottle Inventory",padding=10)
notebook.pack(padx=10, side = BOTTOM)

menubar = Menu(window)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Bottles")
menu1.add_command(label="Grain")
menu1.add_command(label="Barrels")
menubar.add_cascade(label="Inventory", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Production Log")
menu2.add_command(label="Purchase Orders")
menu2.add_command(label="Employee Checkout")
menubar.add_cascade(label="Production and Shipping",menu=menu2)

window.config(menu=menubar)


#create/load and display database
inventory = modules.database()

#RAW MATERIALS table
raw_table = ttk.Treeview(raw_frame, column = ("ID","Item","Amount"), show = "headings",height=600)
raw_table.column("ID", anchor="center", width=250)
raw_table.column("Item", anchor="center", width=250)
raw_table.column("Amount", anchor="center", width=250)
raw_table.heading("#1", text = "ID")
raw_table.heading("#2", text="Item")
raw_table.heading("#3", text="Amount")
raw_table.pack(side=RIGHT,fill = Y)

modules.cur.execute("SELECT * FROM bottles")
rows = modules.cur.fetchall()
for row in rows:
    raw_frame.insert("",END,values = row)

#VIEW (RAW MATERIALS) frame
raw_command_frame = Frame(raw_frame, height = 600,width=50)
raw_view_frame = LabelFrame(raw_command_frame,height = 300, bd = 5, relief= RIDGE, text="View", font="bold")

b1 = Button(raw_view_frame, text = "Bottles", width = 20, height=2)
b1.pack(anchor='center')
b2 = Button(raw_view_frame, text = "Boxes", width = 20, height=2)
b2.pack(anchor='center')
b3 = Button(raw_view_frame, text = "Caps", width = 20, height=2)
b3.pack(anchor='center')
b4 = Button(raw_view_frame, text = "Capsules", width = 20, height=2)
b4.pack(anchor='center')
b5 = Button(raw_view_frame, text = "Labels", width = 20, height=2)
b5.pack(anchor='center')
b6 = Button(raw_view_frame, text = "All", width = 20, height =2)
b6.pack(anchor='center')

#LOGISTICS (RAW MATERIALS) frame
raw_opt_frame = LabelFrame(raw_command_frame,height = 300, text = "Options", bd = 5, relief = RIDGE, font = "bold")

b7 = Button(raw_opt_frame, text="Production" , width = 20, height=2)
b7.pack(anchor='center')
b8 = Button(raw_opt_frame, text = "Raw Materials Received", width=20, height=2)
b8.pack(anchor='center')
b9 = Button(raw_opt_frame, text = "Add Item", width=20, height=2)
b9.pack(anchor='center')
b10 = Button(raw_opt_frame, text = "Remove Item", width=20, height=2)
b10.pack()
b11 = Button(raw_opt_frame, text="Edit Item", width=20, height=2)
b11.pack()

raw_command_frame.pack()
raw_view_frame.pack()
raw_opt_frame.pack()


#BOTTLE table
bottle_table = ttk.Treeview(bottle_frame,column=("ID", "Product", "Amount"), show="headings", height=600)
bottle_table.column("ID", anchor="center", width=250)
bottle_table.column("Product", anchor="center", width=250)
bottle_table.column("Amount", anchor="center", width=250)
bottle_table.heading("#1", text = "ID")
bottle_table.heading("#2", text="Product")
bottle_table.heading("#3", text="Amount")
bottle_table.pack(side=RIGHT,fill = Y)

#VIEW (BOTTLES) frame
bot_command_frame = Frame(bottle_frame,height=600,width=50)
bot_view_frame = LabelFrame(bot_command_frame,height=300, bd=5, relief=RIDGE, text="View", font="bold")

b12 = Button(bot_view_frame, text="Vodka", width=20, height=2)
b12.pack()
b13 = Button(bot_view_frame, text="Whiskey", width=20, height=2)
b13.pack()
b14 = Button(bot_view_frame, text="Rum", width=20, height=2)
b14.pack()
b15 = Button(bot_view_frame, text="Other", width=20, height=2)
b15.pack()
b16 = Button(bot_view_frame, text="All", width=20, height=2)
b16.pack()

#OPTIONS (BOTTLES) frame
bot_opt_frame = LabelFrame(bot_command_frame, height=300, bd=5, relief=RIDGE, text="Options", font="bold")
b17 = Button(bot_opt_frame, text="Add Bottles", width=20, height=2)
b17.pack(anchor='center')
b18 = Button(bot_opt_frame, text="Remove Bottles", width=20, height=2)
b18.pack(anchor='center')

bot_view_frame.pack()
bot_opt_frame.pack()
bot_command_frame.pack()






window.mainloop()
