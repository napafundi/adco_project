from tkinter import *
from tkinter import messagebox, ttk
import sqlite3
from tkcalendar import Calendar
import os
import webbrowser
from PIL import Image, ImageTk
import re

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

def db_update():
    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("UPDATE 'raw materials' SET 'total'= PRINTF('%s%g', '$', amount*price)")
    cur.execute("UPDATE 'bottles' SET 'total'= PRINTF('%s%g', '$', amount*price)")
    cur.execute("UPDATE 'grain inventory' SET 'total'= PRINTF('%s%g', '$', amount*price)")
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
    entries = [x for x in reversed(toplevel_widg.grid_slaves()) if (x.winfo_class() == 'Entry' or x.winfo_class() == 'Menubutton')]
    for entry in entries: #work through add_item entry widgets
        if entry.winfo_class() == 'Entry':
            additions.append(' '.join(word[0].upper() + word[1:] for word in entry.get().split())) #titlecase the string before appending
            num_entries += 1
        elif entry.winfo_class() == 'Menubutton':
            additions.append(add_var.get())
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
    db_update()
    toplevel_widg.destroy()

def view_widget(window,widget,padx,location,sqlite_table,column,item,gui_table):
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
    view_products(sqlite_table,column,item,gui_table)

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
    for index,row in enumerate(rows):
        if (index % 2 == 0):
            tag = 'even'
        else:
            tag = 'odd'
        gui_table.insert("",END,values = row,tags=(tag,))
    gui_table.tag_configure('even', background='#E8E8E8')

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
        Button.__init__(self,master,text=text,command = lambda: view_products(sqlite_table,"Type",text,gui_table),width=20,height=2, font=('Calibri',13,'bold'))

#gives production buttons functionality
class Inventory_Button(Button):
    def __init__(self,master,text,sqlite_table,gui_table):
        self.sqlite_table = sqlite_table
        self.gui_table = gui_table
        Button.__init__(self,master,text=text,width=20,height=2,font=('Calibri',13,'bold'))

class Treeview_Table(ttk.Treeview):
    def __init__(self,master,columns):
        ttk.Treeview.__init__(self,master,columns=columns,show='headings',height=600,style="Custom.Treeview")
        self.width=int(796/(len(columns)))
        self.columns = columns
        for i in range(len(columns)):
            self.column(self.columns[i],anchor='center',width=self.width)
            self.heading(str('#' + str((i+1))),text=self.columns[i])
        self.pack(side=RIGHT,fill=Y)

#iterates through list of items and creates buttons based on 'class_name' object
def button_maker(class_name,list,master_widget,sqlite_table,gui_table):
    for item in list:
        button = class_name(master=master_widget,text=item,sqlite_table=sqlite_table,gui_table=gui_table)
        button.pack(anchor='center')

#create production sheets toplevel window upon clicking the menu option,
#populate with files within production_sheets folder
def sheets_view():
    sheets_window = Toplevel(window)
    files = os.listdir(os.getcwd() + "\\production_sheets")
    window_height = 0
    for file in files:
        mo = fileRegex.search(file)
        file_name = mo.group(1)
        file_label = Sheet_Label(master=sheets_window,text=file_name,file_location= os.getcwd() + "\\production_sheets\\" + file)
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
        mo = fileRegex.search(file)
        file_name = mo.group(1)
        file_label = Sheet_Label(master=labels_window,text=file_name,file_location= os.getcwd() + "\\case_labels\\" + file)
        file_label.pack(padx=10,pady=10,anchor='w')
        window_height += 50
    labels_window.title("Case Labels")
    labels_window.focus()
    x = (screen_width/2) - (500/2)
    y = (screen_height/2) - (500/2)
    labels_window.geometry("%dx%d+%d+%d" % (300,window_height,x,y))
    labels_window.resizable(0,0)

#creates toplevel populated by inputs for items in table
def add_item_view(table):
    window_height = 0
    add_view = Toplevel(window)
    cur = sqlite3.Connection("inventory.db").cursor()
    cur.execute("SELECT * FROM \'" + table + "\'")
    for index,description in enumerate(cur.description): #add labels and entries based on database labels
        if (description[0] != 'type'):
            Label(add_view,text=description[0]).grid(row=index,column=0)
            Entry(add_view).grid(row=index, column=1)
            window_height += 35
            if (description[0].find('date') != -1):  #add calendar selection widget for date entry
                date_index = index
                date_entry = add_view.grid_slaves(row=date_index,column=1)[0]
                date_entry.config(state="readonly")
                def cal_button():
                    top = Toplevel(window)
                    cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                                   cursor="hand2")
                    cal.pack(fill="both", expand=True)
                    def retrieve_date():
                        date_entry.config(state=NORMAL)
                        date_entry.delete(0,END)
                        date_entry.insert(END,cal.selection_get().strftime('%m-%d-%Y'))
                        date_entry.config(state="readonly")
                        top.destroy()
                    Button(top, text="ok", command = retrieve_date).pack() #insert date into date entry
                    top.focus()
                image = Image.open("calendar.png")
                image = image.resize((22,22))
                photo = ImageTk.PhotoImage(image)
                cal_link = Button(add_view,image=photo,command=cal_button)
                cal_link.image = photo
                cal_link.grid(row=index,column=2)
        else:
            Label(add_view,text=description[0]).grid(row=index,column=0)
            global add_var
            add_var = StringVar(window)
            add_var.set(type_options[table][0])
            options = OptionMenu(add_view,add_var,*tuple(type_options[table]))
            options.config(width=14, background = "white")
            options.grid(row=index, column=1)
            window_height += 35
    grid_size = add_view.grid_size()[1] #used to place add/cancel buttons below all other buttons
    Button(add_view,text="Add Item",command = lambda: add_item(table,add_view)).grid(row=grid_size+1,column=1)
    Button(add_view,text="Cancel",command = lambda: add_view.destroy()).grid(row=grid_size+2,column=1)
    add_view.title("Add to " + table)
    add_view.focus()
    x = (screen_width/2) - (500/2)
    y = (screen_height/2) - (500/2)
    add_view.geometry("%dx%d+%d+%d" % (300,window_height,x,y))
    add_view.resizable(0,0)

#used to search for the string literal within a filename that occurs before the file extension (Ex. '.txt')
fileRegex = re.compile(r'''
    ([a-zA-Z0-9_ -]+)
    (.)
    ([a-zA-Z_0-9])''',re.VERBOSE)

#option values for dropdown menus
type_options = {'raw materials': ['Bottles','Boxes','Caps','Capsules','Labels'], 'bottles': ['Vodka','Whiskey','Rum','Other'], 'barrel inventory': ['Bourbon','Rye','Malt','Rum','Other']}

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

#set styles for gui and certain widgets
s = ttk.Style(window)
s.theme_use('xpnative')
s.configure("Treeview", highlightthickness=0, bd=0, font=('Calibri', 11))
s.element_create("Custom.Treeheading.border", "from", "default")
s.layout("Custom.Treeview.Heading", [
    ("Custom.Treeheading.cell", {'sticky': 'nswe'}),
    ("Custom.Treeheading.border", {'sticky':'nswe', 'children': [
        ("Custom.Treeheading.padding", {'sticky':'nswe', 'children': [
            ("Custom.Treeheading.image", {'side':'right', 'sticky':''}),
            ("Custom.Treeheading.text", {'sticky':'we'})
        ]})
    ]}),
])
s.configure("Custom.Treeview.Heading", background="dark slate grey", foreground="white", relief="flat")
s.configure("Treeview.Heading", font=('Calibri', 13,'bold'))
s.configure("TButton",font=('Calibri',13,'bold'))

#create/load and display database
inventory = database()

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

#create raw materials table
raw_materials_table = Treeview_Table(raw_materials_frame,("Type","Item","Amount","Price","Total"))

#show table upon opening application
view_products('raw materials','null','All',raw_materials_table)

#create raw materials command frame and populate with view and options buttons
raw_materials_command_frame = Frame(raw_materials_frame, height = 600,width=50)

raw_materials_view_frame = LabelFrame(raw_materials_command_frame,height = 300, bd = 5, relief= RIDGE, text="View", font="bold")
raw_materials_view_buttons = ["Bottles","Boxes","Caps","Capsules","Labels","All"]
button_maker(View_Button,raw_materials_view_buttons,raw_materials_view_frame,'raw materials',raw_materials_table)

raw_materials_option_frame = LabelFrame(raw_materials_command_frame,height = 300, text = "Options", bd = 5, relief = RIDGE, font = "bold")
Button(raw_materials_option_frame,text="Add Item",width=20,height=2, command = lambda: add_item_view('raw materials'),font=('Calibri',13,'bold')).pack(anchor='center')

raw_materials_command_frame.pack()
raw_materials_view_frame.pack()
raw_materials_option_frame.pack()

#create production table
production_table = Treeview_Table(production_frame,("Date","Product","Amount"))

#TODO: populate production table with production database info

#create production commands frame and populate with an edit button
production_command_frame = Frame(production_frame,height=600,width=50)

production_opt_frame = LabelFrame(production_command_frame,height=300,bd=5,relief=RIDGE,text="Options",font="bold")
Button(production_opt_frame,text="Edit Selection",width=20,height=2).pack(anchor='center')

production_command_frame.pack()
production_opt_frame.pack()

#create materials used table
materials_used_table = Treeview_Table(materials_used_frame,("Product", "Amount","Date"))

#TODO: populate materials used table

#create bottle table
bottle_table = Treeview_Table(bottle_frame,("Type","Product","Amount","Price","Total"))

#create bottle command frame and populate with view and option buttons
bottle_command_frame = Frame(bottle_frame,height=600,width=50)

bottle_view_frame = LabelFrame(bottle_command_frame,height=300, bd=5, relief=RIDGE, text="View", font="bold")
bottle_view_buttons = ["Vodka","Whiskey","Rum","Other","All"]
button_maker(View_Button,bottle_view_buttons,bottle_view_frame,'bottles',bottle_table)

bottle_option_frame = LabelFrame(bottle_command_frame, height=300, bd=5, relief=RIDGE, text="Options", font="bold")
Button(bottle_option_frame,text="Add Item",width=20,height=2, command = lambda: add_item_view('bottles')).pack(anchor='center')

bottle_view_frame.pack()
bottle_option_frame.pack()
bottle_command_frame.pack()

#create grain inventory notebook, populate with tabbed frames
grain_inventory_notebook = ttk.Notebook(window, height=650, width=1024)
grain_inventory_frame = ttk.Frame(grain_inventory_notebook)
grain_inventory_notebook.add(grain_inventory_frame, text="Grain Inventory", padding=10)

#create grain inventory table and pack within grain frame
grain_table = Treeview_Table(grain_inventory_frame,("Order No.","Type","Amount","Price","Total"))

#create grain command frame and populate with option buttons
grain_command_frame = Frame(grain_inventory_frame,height=600,width=50)

grain_option_frame = LabelFrame(grain_command_frame,height=300,bd=5,relief=RIDGE,text="Options",font="bold")
grain_option_buttons = ["Produce Mash","Edit Selection","Mash Production Sheet"]
button_maker(Inventory_Button,grain_option_buttons,grain_option_frame,'grain inventory',grain_table)

grain_command_frame.pack()
grain_option_frame.pack()

#create barrel inventory notebook and populates with tabbed frames
barrel_inventory_notebook = ttk.Notebook(window, height=650, width=1024)
barrel_frame = ttk.Frame(barrel_inventory_notebook)
barrel_inventory_notebook.add(barrel_frame, text="Barrel Inventory",padding=10)

#create barrel inventory table
barrel_table = Treeview_Table(barrel_frame,("Barrel No.","Type","Proof Gallons","Date Filled","Age","Investor"))

#create barrel command frame and populate with view and option buttons
barrel_command_frame = Frame(barrel_frame,height=600,width=50)

barrel_view_frame = LabelFrame(barrel_command_frame,height=300,bd=5,relief=RIDGE,text="View",font="bold")
barrel_view_buttons = ["Bourbon","Rye","Malt","Other","All"]
button_maker(View_Button,barrel_view_buttons,barrel_view_frame,'barrel inventory',barrel_table)

barrel_option_frame = LabelFrame(barrel_command_frame,height=300,bd=5,relief=RIDGE,text="Options",font="bold")
Button(barrel_option_frame,text="Add Barrel",width=20,height=2,command = lambda: add_item_view('barrel inventory')).pack(anchor='center')

barrel_command_frame.pack()
barrel_view_frame.pack()
barrel_option_frame.pack()

#create purchase orders notebook with tabbed frames
purchase_orders_notebook = ttk.Notebook(window,height=650,width=1024)
purchase_orders_frame = Frame(purchase_orders_notebook)
purchase_orders_notebook.add(purchase_orders_frame,text="Purchase Orders",padding=10)

#create purchase orders table
purchase_orders_table = Treeview_Table(purchase_orders_frame,("Date","Product","Amount","Price","Total","Destination","PO No."))

#create purchase orders command frame and populate with option buttons
purchase_orders_command_frame = Frame(purchase_orders_frame,height=600,width=50)

purchase_orders_option_frame = LabelFrame(purchase_orders_command_frame,height=300,bd=5,relief=RIDGE,text="Options",font='bold')
purchase_orders_option_buttons = ["Create Purchase Order","View Purchase Order","Edit Selection"]
button_maker(Inventory_Button,purchase_orders_option_buttons,purchase_orders_option_frame,'purchase orders',purchase_orders_table)

purchase_orders_command_frame.pack()
purchase_orders_option_frame.pack()

#create employee transactions notebook and populate with tabbed frames
employee_transactions_notebook = ttk.Notebook(window,height=650,width=1024)
employee_transactions_frame = Frame(employee_transactions_notebook)
employee_transactions_notebook.add(employee_transactions_frame,text="Employee Transactions",padding=10)

#create employee transactions table
employee_transactions_table = Treeview_Table(employee_transactions_frame,("Date","Product","Amount","Employee"))

#create employee transactions command frame and populate with option buttons
employee_transactions_command_frame = Frame(employee_transactions_frame,height=600,width=50)

employee_transactions_options_frame = LabelFrame(employee_transactions_command_frame,height=300,bd=5,relief=RIDGE,text="Options",font="bold")
employee_transactions_options_buttons = ["Checkout Bottles","Edit Selection"]
button_maker(Inventory_Button,employee_transactions_options_buttons,employee_transactions_options_frame,'employee transactions',employee_transactions_table)

employee_transactions_command_frame.pack()
employee_transactions_options_frame.pack()

#create menu bar at the top of the gui, populate with clickable tabs
menubar = Menu(window)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Bottles", command=lambda: view_widget(window,bottle_inventory_notebook,10,BOTTOM,'raw materials','null','All',raw_materials_table))
menu1.add_command(label="Grain", command=lambda: view_widget(window,grain_inventory_notebook,10,BOTTOM,'grain inventory','null','All',grain_table))
menu1.add_command(label="Barrels", command=lambda: view_widget(window,barrel_inventory_notebook,10,BOTTOM,'barrel inventory','null','All',barrel_table))
menubar.add_cascade(label="Inventory", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Purchase Orders", command=lambda: view_widget(window,purchase_orders_notebook,10,BOTTOM,'purchase orders','null','All',purchase_orders_table))
menu2.add_command(label="Employee Transactions", command=lambda: view_widget(window,employee_transactions_notebook,10,BOTTOM,'employee transactions','null','All',employee_transactions_table))
menubar.add_cascade(label="Shipping and Transactions",menu=menu2)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="Production Sheets", command=sheets_view)
menu3.add_command(label="Case Labels", command=labels_view)
menubar.add_cascade(label="Files", menu=menu3)

window.config(menu=menubar)
window.mainloop()
