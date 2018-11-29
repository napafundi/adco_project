from tkinter import *
import sqlite3
import modules
from tkinter import ttk
import os
import webbrowser

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

#BOTTLE INV
bottle_inv = ttk.Notebook(window, height = 650, width = 1024)
raw_frame = ttk.Frame(bottle_inv)
bottle_frame = ttk.Frame(bottle_inv)
production_frame = ttk.Frame(bottle_inv)
raw_materials_used = ttk.Frame(bottle_inv)
bottle_inv.add(raw_frame, text = "Raw Materials",padding=10)
bottle_inv.add(production_frame, text="Production Log",padding=10)
bottle_inv.add(raw_materials_used, text="Materials Used", padding=10)
bottle_inv.add(bottle_frame, text = "Bottle Inventory",padding=10)
bottle_inv.pack(padx=10, side = BOTTOM)

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

#VIEW (RAW MATERIALS)
raw_command_frame = Frame(raw_frame, height = 600,width=50)
raw_view_frame = LabelFrame(raw_command_frame,height = 300, bd = 5, relief= RIDGE, text="View", font="bold")

br1 = Button(raw_view_frame, text = "Bottles", width = 20, height=2)
br1.pack(anchor='center')
br2 = Button(raw_view_frame, text = "Boxes", width = 20, height=2)
br2.pack(anchor='center')
br3 = Button(raw_view_frame, text = "Caps", width = 20, height=2)
br3.pack(anchor='center')
br4 = Button(raw_view_frame, text = "Capsules", width = 20, height=2)
br4.pack(anchor='center')
br5 = Button(raw_view_frame, text = "Labels", width = 20, height=2)
br5.pack(anchor='center')
br6 = Button(raw_view_frame, text = "All", width = 20, height =2)
br6.pack(anchor='center')

#OPTIONS (RAW MATERIALS)
raw_opt_frame = LabelFrame(raw_command_frame,height = 300, text = "Options", bd = 5, relief = RIDGE, font = "bold")

br7 = Button(raw_opt_frame, text="Production" , width = 20, height=2)
br7.pack(anchor='center')
br8 = Button(raw_opt_frame, text = "Raw Materials Received", width=20, height=2)
br8.pack(anchor='center')
br9 = Button(raw_opt_frame, text = "Add Item", width=20, height=2)
br9.pack(anchor='center')
br10 = Button(raw_opt_frame, text = "Remove Item", width=20, height=2)
br10.pack()
br11 = Button(raw_opt_frame, text="Edit Selection", width=20, height=2)
br11.pack()

raw_command_frame.pack()
raw_view_frame.pack()
raw_opt_frame.pack()

#PRODUCTION table
production_table = ttk.Treeview(production_frame, column=("Date","Product","Amount"),show="headings",height=600)
production_table.column("Date",anchor="center",width=250)
production_table.column("Product",anchor="center",width=250)
production_table.column("Amount",anchor="center",width=250)
production_table.heading("#1", text="Date")
production_table.heading("#2", text="Product")
production_table.heading("#3", text="Amount")
production_table.pack(side=RIGHT, fill=Y)

#OPTIONS (PRODUCTION LOG)
production_command_frame = Frame(production_frame,height=600,width=50)
production_opt_frame = LabelFrame(production_command_frame,height=300,bd=5,relief=RIDGE,text="Options",font="bold")

bp1 = Button(production_opt_frame,text="Edit Selection",width=20,height=2)
bp1.pack(anchor='center')

production_command_frame.pack()
production_opt_frame.pack()

#MATERIALS USED table
bottle_table = ttk.Treeview(raw_materials_used,column=("ID", "Product", "Amount","Date"), show="headings", height=600)
bottle_table.column("ID", anchor="center", width=200)
bottle_table.column("Product", anchor="center", width=200)
bottle_table.column("Amount", anchor="center", width=200)
bottle_table.column("Date", anchor="center", width=200)
bottle_table.heading("#1", text = "ID")
bottle_table.heading("#2", text="Product")
bottle_table.heading("#3", text="Amount")
bottle_table.heading("#4", text="Date")
bottle_table.pack(fill='both')

#BOTTLE table
bottle_table = ttk.Treeview(bottle_frame,column=("ID", "Product", "Amount"), show="headings", height=600)
bottle_table.column("ID", anchor="center", width=250)
bottle_table.column("Product", anchor="center", width=250)
bottle_table.column("Amount", anchor="center", width=250)
bottle_table.heading("#1", text = "ID")
bottle_table.heading("#2", text="Product")
bottle_table.heading("#3", text="Amount")
bottle_table.pack(side=RIGHT,fill = Y)

#VIEW (BOTTLES)
bot_command_frame = Frame(bottle_frame,height=600,width=50)
bot_view_frame = LabelFrame(bot_command_frame,height=300, bd=5, relief=RIDGE, text="View", font="bold")

bb1 = Button(bot_view_frame, text="Vodka", width=20, height=2)
bb1.pack()
bb2 = Button(bot_view_frame, text="Whiskey", width=20, height=2)
bb2.pack()
bb3 = Button(bot_view_frame, text="Rum", width=20, height=2)
bb3.pack()
bb4 = Button(bot_view_frame, text="Other", width=20, height=2)
bb4.pack()
bb5 = Button(bot_view_frame, text="All", width=20, height=2)
bb5.pack()

#OPTIONS (BOTTLES)
bot_opt_frame = LabelFrame(bot_command_frame, height=300, bd=5, relief=RIDGE, text="Options", font="bold")

bb6 = Button(bot_opt_frame, text="Add Item", width=20, height=2)
bb6.pack(anchor='center')
bb7 = Button(bot_opt_frame, text="Remove Item", width=20, height=2)
bb7.pack()
bb8 = Button(bot_opt_frame, text="Edit Selection", width=20, height=2)
bb8.pack(anchor='center')

bot_view_frame.pack()
bot_opt_frame.pack()
bot_command_frame.pack()

#GRAIN INV
grain_inv = ttk.Notebook(window, height=650, width=1024)
grain_frame = ttk.Frame(grain_inv)
grain_inv.add(grain_frame, text="Grain Inventory", padding=10)

#GRAIN table
grain_table = ttk.Treeview(grain_frame, column=("ID","Type","Amount","Order No."),show="headings",height=600)
grain_table.column("ID",anchor="center",width=187)
grain_table.column("Type",anchor="center",width=187)
grain_table.column("Amount",anchor="center",width=187)
grain_table.column("Order No.",anchor="center",width=187)
grain_table.heading("#1", text="ID")
grain_table.heading("#2", text="Type")
grain_table.heading("#3", text="Amount")
grain_table.heading("#4", text="Order No.")
grain_table.pack(side=RIGHT, fill=Y)

#OPTIONS (GRAIN)
grain_command_frame = Frame(grain_frame,height=600,width=50)
grain_opt_frame = LabelFrame(grain_command_frame,height=300,bd=5,relief=RIDGE,text="Options",font="bold")

bg1 = Button(grain_opt_frame,text="Produce Mash",width=20,height=2)
bg1.pack(anchor='center')
bg2 = Button(grain_opt_frame,text="Edit Selection",width=20,height=2)
bg2.pack(anchor='center')
bg3 = Button(grain_opt_frame,text="Mash Production Sheet",width=20,height=2)
bg3.pack()

grain_command_frame.pack()
grain_opt_frame.pack()

#BARREL INV
barrel_inv = ttk.Notebook(window, height=650, width=1024)
barrel_frame = ttk.Frame(barrel_inv)
barrel_inv.add(barrel_frame, text="Barrel Inventory",padding=10)

#BARREL table
barrel_table = ttk.Treeview(barrel_frame, column=("Barrel No.","Spirit","Proof Gallons","Date Filled","Age","Investor"),show="headings",height=600)
barrel_table.column("Barrel No.",anchor="center",width=125)
barrel_table.column("Spirit",anchor="center",width=125)
barrel_table.column("Proof Gallons",anchor="center",width=125)
barrel_table.column("Date Filled",anchor="center",width=125)
barrel_table.column("Age",anchor="center",width=125)
barrel_table.column("Investor",anchor="center",width=125)
barrel_table.heading("#1", text="Barrel No.")
barrel_table.heading("#2", text="Spirit")
barrel_table.heading("#3", text="Proof Gallons")
barrel_table.heading("#4", text="Date Filled")
barrel_table.heading("#5", text="Age")
barrel_table.heading("#6", text="Investor")
barrel_table.pack(side=RIGHT, fill=Y)

#VIEW (BARRELS)
barrel_command_frame = Frame(barrel_frame,height=600,width=50)
barrel_view_frame = LabelFrame(barrel_command_frame,height=300,bd=5,relief=RIDGE,text="View",font="bold")

bba1 = Button(barrel_view_frame,text="Bourbon",width=20,height=2)
bba1.pack(anchor='center')
bba2 = Button(barrel_view_frame,text="Rye",width=20,height=2)
bba2.pack(anchor='center')
bba3 = Button(barrel_view_frame,text="Malt",width=20,height=2)
bba3.pack(anchor='center')
bba4 = Button(barrel_view_frame,text="Other",width=20,height=2)
bba4.pack(anchor='center')
bba5 = Button(barrel_view_frame,text="All",width=20,height=2)
bba5.pack(anchor='center')

#OPTIONS (BARRELS)

barrel_opt_frame = LabelFrame(barrel_command_frame,height=300,bd=5,relief=RIDGE,text="Options",font="bold")

bba6 = Button(barrel_opt_frame, text="Fill Barrel",width=20,height=2)
bba6.pack(anchor='center')
bba7 = Button(barrel_opt_frame,text="Empty Barrel",width=20,height=2)
bba7.pack(anchor='center')
bba8 = Button(barrel_opt_frame,text="Edit Selecton",width=20,height=2)
bba8.pack(anchor='center')

barrel_command_frame.pack()
barrel_view_frame.pack()
barrel_opt_frame.pack()



#PURCHASE ORDERS
purchase_orders = ttk.Notebook(window,height=650,width=1024)
po_frame = Frame(purchase_orders)
purchase_orders.add(po_frame,text="Purchase Orders",padding=10)

#PURCHASE ORDERS table
po_table = ttk.Treeview(po_frame, column=("Date","Product","Amount","Destination","PO No."),show="headings",height=600)
po_table.column("Date",anchor="center",width=150)
po_table.column("Product",anchor="center",width=150)
po_table.column("Amount",anchor="center",width=150)
po_table.column("Destination",anchor="center",width=150)
po_table.column("PO No.",anchor="center",width=150)
po_table.heading("#1", text="Date")
po_table.heading("#2", text="Product")
po_table.heading("#3", text="Amount")
po_table.heading("#4", text="Destination")
po_table.heading("#5", text="PO No.")
po_table.pack(side=RIGHT, fill=Y)

#OPTIONS (PURCHASE ORDERS)
po_command_frame = Frame(po_frame,height=600,width=50)
po_opt_frame = LabelFrame(po_command_frame,height=300,bd=5,relief=RIDGE,text="Options",font='bold')

bpo1 = Button(po_opt_frame,text="Create Purchase Order",width=20,height=2)
bpo1.pack(anchor='center')
bpo2 = Button(po_opt_frame,text="View Purchase Order",width=20,height=2)
bpo2.pack(anchor='center')
bpo3 = Button(po_opt_frame,text="Edit Selection",width=20,height=2)
bpo3.pack(anchor='center')

po_command_frame.pack()
po_opt_frame.pack()

#EMPLOYEE TRANSACTIONS
employee_transactions = ttk.Notebook(window,height=650,width=1024)
emp_trans_frame = Frame(employee_transactions)
employee_transactions.add(emp_trans_frame,text="Employee Transactions",padding=10)

#EMPLOYEE TRANSACTIONS table
emp_trans_table = ttk.Treeview(emp_trans_frame, column=("Date","Product","Amount","Employee"),show="headings",height=600)
emp_trans_table.column("Date",anchor="center",width=187)
emp_trans_table.column("Product",anchor="center",width=187)
emp_trans_table.column("Amount",anchor="center",width=187)
emp_trans_table.column("Employee",anchor="center",width=187)
emp_trans_table.heading("#1", text="Date")
emp_trans_table.heading("#2", text="Product")
emp_trans_table.heading("#3", text="Amount")
emp_trans_table.heading("#4", text="Employee")
emp_trans_table.pack(side=RIGHT, fill=Y)

#OPTIONS (EMPLOYEE TRANSACTIONS)
emp_trans_command_frame = Frame(emp_trans_frame,height=600,width=50)
emp_trans_opt_frame = LabelFrame(emp_trans_command_frame,height=300,bd=5,relief=RIDGE,text="Options",font="bold")

bet1 = Button(emp_trans_opt_frame,text="Checkout Bottles",width=20,height=2)
bet1.pack(anchor='center')
bet2 = Button(emp_trans_opt_frame,text="Edit Selection",width=20,height=2)
bet2.pack(anchor='center')

emp_trans_command_frame.pack()
emp_trans_opt_frame.pack()

#PRODUCTION SHEETS
sheets_list = ["hello.txt"]

def view_sheet(file):
    location = os.getcwd()
    file = webbrowser.open_new(location + '\\' + file)

def sheets_view():
    sheets_window = Toplevel(window)
    link = modules.Link_Button(sheets_window,text="Hello.txt",action=view_sheet)
    link.pack()
    sheets_window.title("Production Sheets")
    sheets_window.focus()
    x = (screen_width/2) - (500/2)
    y = (screen_height/2) - (500/2)
    sheets_window.geometry("%dx%d+%d+%d" % (500,500,x,y))
    sheets_window.resizable(0,0)

#MENU BAR
menubar = Menu(window)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Bottles", command=lambda: modules.view_widget(window,bottle_inv,10,BOTTOM))
menu1.add_command(label="Grain", command=lambda: modules.view_widget(window,grain_inv,10,BOTTOM))
menu1.add_command(label="Barrels", command=lambda: modules.view_widget(window,barrel_inv,10,BOTTOM))
menubar.add_cascade(label="Inventory", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Purchase Orders", command=lambda: modules.view_widget(window,purchase_orders,10,BOTTOM))
menu2.add_command(label="Employee Transactions", command=lambda: modules.view_widget(window,employee_transactions,10,BOTTOM))
menubar.add_cascade(label="Shipping and Transactions",menu=menu2)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="Production Sheets", command=sheets_view)
menu3.add_command(label="Case Labels")
menubar.add_cascade(label="Files", menu=menu3)

window.config(menu=menubar)








window.mainloop()
