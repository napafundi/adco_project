from tkinter import *
import sqlite3
import modules
from tkinter import ttk
import os
import webbrowser

#create root window, resize based on user's screen info
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

#set theme for gui
s = ttk.Style()
s.theme_use('xpnative')

#create/load and display database
inventory = modules.database()

#create bottle inventory notebook, populate with tabbed frames
bottle_inventory_notebook = ttk.Notebook(window, height = 650, width = 1024)
raw_materials_frame = ttk.Frame(bottle_inventory_notebook)
bottle_frame = ttk.Frame(bottle_inventory_notebook)
production_frame = ttk.Frame(bottle_inventory_notebook)
materials_used_frame = ttk.Frame(bottle_inventory_notebook)
bottle_inventory_notebook.add(raw_materials_frame, text = "Raw Materials",padding=10)
bottle_inventory_notebook.add(production_frame, text="Production Log",padding=10)
bottle_inventory_notebook.add(materials_used_frame, text="Materials Used", padding=10)
bottle_inventory_notebook.add(bottle_frame, text = "Bottle Inventory",padding=10)
bottle_inventory_notebook.pack(padx=10, side = BOTTOM)

#create raw materials table and populate with data from raw materials database
raw_materials_table = ttk.Treeview(raw_materials_frame, column = ("ID","Type","Item","Amount","Price","Total"), show = "headings",height=600)
w=int(796/(len(raw_materials_table['columns'])))
raw_materials_table.column("ID", anchor="center", width=w)
raw_materials_table.column("Type", anchor="center", width=w)
raw_materials_table.column("Item", anchor="center", width=w)
raw_materials_table.column("Amount", anchor="center", width=w)
raw_materials_table.column("Price", anchor="center", width=w)
raw_materials_table.column("Total", anchor="center", width=w)
raw_materials_table.heading("#1", text = "ID")
raw_materials_table.heading("#2", text = "Type")
raw_materials_table.heading("#3", text="Item")
raw_materials_table.heading("#4", text="Amount")
raw_materials_table.heading("#5", text = "Price")
raw_materials_table.heading("#6", text = "Total")
raw_materials_table.pack(side=RIGHT,fill = Y)

modules.cur.execute("SELECT * FROM 'raw materials'")
rows = modules.cur.fetchall()
for row in rows:
    raw_materials_table.insert("",END,values = row)

#create raw materials command frame and populate with view and options buttons
raw_materials_command_frame = Frame(raw_materials_frame, height = 600,width=50)

raw_materials_view_frame = LabelFrame(raw_materials_command_frame,height = 300, bd = 5, relief= RIDGE, text="View", font="bold")
raw_materials_view_buttons = ["Bottles","Boxes","Caps","Capsules","Labels","All"]
modules.button_maker(modules.View_Button,raw_materials_view_buttons,raw_materials_view_frame,'raw materials',raw_materials_table)

raw_materials_option_frame = LabelFrame(raw_materials_command_frame,height = 300, text = "Options", bd = 5, relief = RIDGE, font = "bold")
raw_materials_option_buttons = ["Production","Raw Materials Received","Add Item","Remove Item","Edit Selection"]
modules.button_maker(modules.Inventory_Button,raw_materials_option_buttons,raw_materials_option_frame,'raw materials',raw_materials_table)

raw_materials_command_frame.pack()
raw_materials_view_frame.pack()
raw_materials_option_frame.pack()

#create production table
production_table = ttk.Treeview(production_frame, column=("Date","Product","Amount"),show="headings",height=600)
w = int(796/ (len(production_table['columns'])))
production_table.column("Date",anchor="center",width=w)
production_table.column("Product",anchor="center",width=w)
production_table.column("Amount",anchor="center",width=w)
production_table.heading("#1", text="Date")
production_table.heading("#2", text="Product")
production_table.heading("#3", text="Amount")
production_table.pack(side=RIGHT, fill=Y)

#TODO: populate production table with production database info

#create production commands frame and populate with an edit button
production_command_frame = Frame(production_frame,height=600,width=50)

production_opt_frame = LabelFrame(production_command_frame,height=300,bd=5,relief=RIDGE,text="Options",font="bold")
bp1 = Button(production_opt_frame,text="Edit Selection",width=20,height=2)
bp1.pack(anchor='center')

production_command_frame.pack()
production_opt_frame.pack()

#create materials used table
materials_used_table = ttk.Treeview(materials_used_frame,column=("ID", "Product", "Amount","Date"), show="headings", height=600)
w=int(796/(len(materials_used_table['columns'])))
materials_used_table.column("ID", anchor="center", width=w)
materials_used_table.column("Product", anchor="center", width=w)
materials_used_table.column("Amount", anchor="center", width=w)
materials_used_table.column("Date", anchor="center", width=w)
materials_used_table.heading("#1", text = "ID")
materials_used_table.heading("#2", text="Product")
materials_used_table.heading("#3", text="Amount")
materials_used_table.heading("#4", text="Date")
materials_used_table.pack(fill='both')

#TODO: populate materials used table

#create bottle table
bottle_table = ttk.Treeview(bottle_frame,column=("ID","Type","Product","Amount","Price","Total"), show="headings", height=600)
w = int(796/ (len(bottle_table['columns'])))
bottle_table.column("ID", anchor="center", width=w)
bottle_table.column("Type", anchor="center", width=w)
bottle_table.column("Product", anchor="center", width=w)
bottle_table.column("Amount", anchor="center", width=w)
bottle_table.column("Price", anchor="center", width=w)
bottle_table.column("Total", anchor="center", width=w)
bottle_table.heading("#1", text="ID")
bottle_table.heading("#2", text="Type")
bottle_table.heading("#3", text="Product")
bottle_table.heading("#4", text="Amount")
bottle_table.heading("#5", text="Price")
bottle_table.heading("#6", text="Total")
bottle_table.pack(side=RIGHT,fill = Y)

#create bottle command frame and populate with view and option buttons
bottle_command_frame = Frame(bottle_frame,height=600,width=50)

bottle_view_frame = LabelFrame(bottle_command_frame,height=300, bd=5, relief=RIDGE, text="View", font="bold")
bottle_view_buttons = ["Vodka","Whiskey","Rum","Other","All"]
modules.button_maker(modules.View_Button,bottle_view_buttons,bottle_view_frame,'bottles',bottle_table)

bottle_option_frame = LabelFrame(bottle_command_frame, height=300, bd=5, relief=RIDGE, text="Options", font="bold")
bottle_option_buttons = ["Add Item","Remove Item","Edit Selection"]
modules.button_maker(modules.Inventory_Button,bottle_option_buttons,bottle_option_frame,'bottles',bottle_table)

bottle_view_frame.pack()
bottle_option_frame.pack()
bottle_command_frame.pack()

#create grain inventory notebook, populate with tabbed frames
grain_inventory_notebook = ttk.Notebook(window, height=650, width=1024)
grain_inventory_frame = ttk.Frame(grain_inventory_notebook)
grain_inventory_notebook.add(grain_inventory_frame, text="Grain Inventory", padding=10)

#create grain inventory table and pack within grain frame
grain_table = ttk.Treeview(grain_inventory_frame, column=("ID","Order No.","Type","Amount","Price","Total"),show="headings",height=600)
w=int(796/(len(grain_table['columns'])))
grain_table.column("ID",anchor="center",width=w)
grain_table.column("Order No.",anchor="center",width=w)
grain_table.column("Type",anchor="center",width=w)
grain_table.column("Amount",anchor="center",width=w)
grain_table.column("Price",anchor="center",width=w)
grain_table.column("Total",anchor='center',width=w)
grain_table.heading("#1", text="ID")
grain_table.heading("#2", text="Order No.")
grain_table.heading("#3", text="Type")
grain_table.heading("#4", text="Amount")
grain_table.heading("#5", text="Price")
grain_table.heading("#6", text="Total")
grain_table.pack(side=RIGHT, fill=Y)

#create grain command frame and populate with option buttons
grain_command_frame = Frame(grain_inventory_frame,height=600,width=50)

grain_option_frame = LabelFrame(grain_command_frame,height=300,bd=5,relief=RIDGE,text="Options",font="bold")
grain_option_buttons = ["Produce Mash","Edit Selection","Mash Production Sheet"]
modules.button_maker(modules.Inventory_Button,grain_option_buttons,grain_option_frame,'grain inventory',grain_table)

grain_command_frame.pack()
grain_option_frame.pack()

#create barrel inventory notebook and populates with tabbed frames
barrel_inventory_notebook = ttk.Notebook(window, height=650, width=1024)
barrel_frame = ttk.Frame(barrel_inventory_notebook)
barrel_inventory_notebook.add(barrel_frame, text="Barrel Inventory",padding=10)

#create barrel inventory table
barrel_table = ttk.Treeview(barrel_frame, column=("Barrel No.","Type","Proof Gallons","Date Filled","Age","Investor"),show="headings",height=600)
w=int(796/(len(barrel_table['columns'])))
barrel_table.column("Barrel No.",anchor="center",width=w)
barrel_table.column("Type",anchor="center",width=w)
barrel_table.column("Proof Gallons",anchor="center",width=w)
barrel_table.column("Date Filled",anchor="center",width=w)
barrel_table.column("Age",anchor="center",width=w)
barrel_table.column("Investor",anchor="center",width=w)
barrel_table.heading("#1", text="Barrel No.")
barrel_table.heading("#2", text="Type")
barrel_table.heading("#3", text="Proof Gallons")
barrel_table.heading("#4", text="Date Filled")
barrel_table.heading("#5", text="Age")
barrel_table.heading("#6", text="Investor")
barrel_table.pack(side=RIGHT, fill=Y)

#create barrel command frame and populate with view and option buttons
barrel_command_frame = Frame(barrel_frame,height=600,width=50)

barrel_view_frame = LabelFrame(barrel_command_frame,height=300,bd=5,relief=RIDGE,text="View",font="bold")
barrel_view_buttons = ["Bourbon","Rye","Malt","Other","All"]
modules.button_maker(modules.View_Button,barrel_view_buttons,barrel_view_frame,'barrel inventory',barrel_table)

barrel_option_frame = LabelFrame(barrel_command_frame,height=300,bd=5,relief=RIDGE,text="Options",font="bold")
barrel_option_buttons = ["Fill Barrel","Empty Barrel","Edit Selection"]
modules.button_maker(modules.Inventory_Button,barrel_option_buttons,barrel_option_frame,'barrel inventory',barrel_table)

barrel_command_frame.pack()
barrel_view_frame.pack()
barrel_option_frame.pack()

#create purchase orders notebook with tabbed frames
purchase_orders_notebook = ttk.Notebook(window,height=650,width=1024)
purchase_orders_frame = Frame(purchase_orders_notebook)
purchase_orders_notebook.add(purchase_orders_frame,text="Purchase Orders",padding=10)

#create purchase orders table
purchase_orders_table = ttk.Treeview(purchase_orders_frame, column=("Date","Product","Amount","Price","Total","Destination","PO No."),show="headings",height=600)
w=int(796/(len(purchase_orders_table['columns'])))
purchase_orders_table.column("Date",anchor="center",width=w)
purchase_orders_table.column("Product",anchor="center",width=w)
purchase_orders_table.column("Amount",anchor="center",width=w)
purchase_orders_table.column("Price",anchor="center",width=w)
purchase_orders_table.column("Total",anchor="center",width=w)
purchase_orders_table.column("Destination",anchor="center",width=w)
purchase_orders_table.column("PO No.",anchor="center",width=w)
purchase_orders_table.heading("#1", text="Date")
purchase_orders_table.heading("#2", text="Product")
purchase_orders_table.heading("#3", text="Amount")
purchase_orders_table.heading("#4", text="Price")
purchase_orders_table.heading("#5", text="Total")
purchase_orders_table.heading("#6", text="Destination")
purchase_orders_table.heading("#7", text="PO No.")
purchase_orders_table.pack(side=RIGHT, fill=Y)

#create purchase orders command frame and populate with option buttons
purchase_orders_command_frame = Frame(purchase_orders_frame,height=600,width=50)

purchase_orders_option_frame = LabelFrame(purchase_orders_command_frame,height=300,bd=5,relief=RIDGE,text="Options",font='bold')
purchase_orders_option_buttons = ["Create Purchase Order","View Purchase Order","Edit Selection"]
modules.button_maker(modules.Inventory_Button,purchase_orders_option_buttons,purchase_orders_option_frame,'purchase orders',purchase_orders_table)

purchase_orders_command_frame.pack()
purchase_orders_option_frame.pack()

#create employee transactions notebook and populate with tabbed frames
employee_transactions_notebook = ttk.Notebook(window,height=650,width=1024)
employee_transactions_frame = Frame(employee_transactions_notebook)
employee_transactions_notebook.add(employee_transactions_frame,text="Employee Transactions",padding=10)

#create employee transactions table
employee_transactions_table = ttk.Treeview(employee_transactions_frame, column=("Date","Product","Amount","Employee"),show="headings",height=600)
w=int(796/(len(employee_transactions_table['columns'])))
employee_transactions_table.column("Date",anchor="center",width=w)
employee_transactions_table.column("Product",anchor="center",width=w)
employee_transactions_table.column("Amount",anchor="center",width=w)
employee_transactions_table.column("Employee",anchor="center",width=w)
employee_transactions_table.heading("#1", text="Date")
employee_transactions_table.heading("#2", text="Product")
employee_transactions_table.heading("#3", text="Amount")
employee_transactions_table.heading("#4", text="Employee")
employee_transactions_table.pack(side=RIGHT, fill=Y)

#create employee transactions command frame and populate with option buttons
employee_transactions_command_frame = Frame(employee_transactions_frame,height=600,width=50)

employee_transactions_options_frame = LabelFrame(employee_transactions_command_frame,height=300,bd=5,relief=RIDGE,text="Options",font="bold")
employee_transactions_options_buttons = ["Checkout Bottles","Edit Selection"]
modules.button_maker(modules.Inventory_Button,employee_transactions_options_buttons,employee_transactions_options_frame,'employee transactions',employee_transactions_table)

employee_transactions_command_frame.pack()
employee_transactions_options_frame.pack()

#create production sheets toplevel window upon clicking the menu option,
#populate with files within production_sheets folder
def sheets_view():
    sheets_window = Toplevel(window)
    files = os.listdir(os.getcwd() + "\\production_sheets")
    window_height = 0
    for file in files:
        mo = modules.fileRegex.search(file)
        file_name = mo.group(1)
        file_label = modules.Sheet_Label(master=sheets_window,text=file_name,file_location= os.getcwd() + "\\production_sheets\\" + file)
        file_label.pack(padx=10,pady=10,anchor='w')
        window_height += 50
    sheets_window.title("Production Sheets")
    sheets_window.focus()
    x = (screen_width/2) - (500/2)
    y = (screen_height/2) - (500/2)
    sheets_window.geometry("%dx%d+%d+%d" % (300,window_height,x,y))
    sheets_window.resizable(0,0)

#create case labels toplevel window upon clicking the menu option,
#populate with files within case_labels folder
def labels_view():
    labels_window = Toplevel(window)
    files = os.listdir(os.getcwd() + "\\case_labels")
    window_height = 0
    for file in files:
        mo = modules.fileRegex.search(file)
        file_name = mo.group(1)
        file_label = modules.Sheet_Label(master=labels_window,text=file_name,file_location= os.getcwd() + "\\case_labels\\" + file)
        file_label.pack(padx=10,pady=10,anchor='w')
        window_height += 50
    labels_window.title("Case Labels")
    labels_window.focus()
    x = (screen_width/2) - (500/2)
    y = (screen_height/2) - (500/2)
    labels_window.geometry("%dx%d+%d+%d" % (300,window_height,x,y))
    labels_window.resizable(0,0)

#create menu bar at the top of the gui, populate with clickable tabs
menubar = Menu(window)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Bottles", command=lambda: modules.view_widget(window,bottle_inventory_notebook,10,BOTTOM))
menu1.add_command(label="Grain", command=lambda: modules.view_widget(window,grain_inventory_notebook,10,BOTTOM))
menu1.add_command(label="Barrels", command=lambda: modules.view_widget(window,barrel_inventory_notebook,10,BOTTOM))
menubar.add_cascade(label="Inventory", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Purchase Orders", command=lambda: modules.view_widget(window,purchase_orders_notebook,10,BOTTOM))
menu2.add_command(label="Employee Transactions", command=lambda: modules.view_widget(window,employee_transactions_notebook,10,BOTTOM))
menubar.add_cascade(label="Shipping and Transactions",menu=menu2)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="Production Sheets", command=sheets_view)
menu3.add_command(label="Case Labels", command=labels_view)
menubar.add_cascade(label="Files", menu=menu3)

window.config(menu=menubar)

modules.add_item()

modules.conn.close()
window.mainloop()
