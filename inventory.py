from tkinter import *
from tkinter import messagebox, ttk
import sqlite3
from tkcalendar import Calendar
import os
import webbrowser
from PIL import Image, ImageTk
import re
from datetime import datetime
import math

def database():
    global conn,cur
    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'raw_materials' (type TEXT,item TEXT, amount INTEGER, price REAL, total TEXT)")
    cur.execute("UPDATE 'raw_materials' SET total= PRINTF('%s%.2f', '$', amount*price)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'production_log' (product TEXT, amount INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'bottles' (type TEXT, product TEXT, amount INTEGER,price REAL, total TEXT)")
    cur.execute("UPDATE 'bottles' SET total= PRINTF('%s%.2f', '$', amount*price)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'grain' ('order_number' TEXT, type TEXT, amount INTEGER,price REAL, total TEXT)")
    cur.execute("UPDATE 'grain' SET total= PRINTF('%s%.2f', '$', amount*price)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'barrels' ('barrel_number' TEXT, type TEXT,'pg' INTEGER, 'date_filled' DATE, age TEXT,investor TEXT)")
    cur.execute("UPDATE 'barrels' SET age= PRINTF('%d years, %d months',(julianday('now') - julianday(date_filled)) / 365,(julianday('now') - julianday(date_filled)) % 365 / 30)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'purchase_orders' (date DATE,product TEXT, amount INTEGER, price REAL, total REAL, destination TEXT, 'po_number' TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'employee_transactions' (date DATE,product TEXT, amount INTEGER, employee TEXT)")
    conn.commit()
    conn.close()

def db_update():
    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("UPDATE 'raw_materials' SET total= PRINTF('%s%g', '$', amount*price)")
    cur.execute("UPDATE 'bottles' SET total= PRINTF('%s%g', '$', amount*price)")
    cur.execute("UPDATE 'grain' SET total= PRINTF('%s%g', '$', amount*price)")
    cur.execute("UPDATE 'barrels' SET age= PRINTF('%d years, %d months',(julianday('now') - julianday(date_filled)) / 365,(julianday('now') - julianday(date_filled)) % 365 / 30)")
    conn.commit()
    conn.close()

def raw_edit(sql_edit):
    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("UPDATE 'raw_materials' SET type=?,item=?,amount=?,price=?,total=? WHERE type=? AND item=? AND amount=? AND price=? AND total=?", sql_edit)
    conn.commit()
    conn.close()

def view_widget(window,widget,location,sqlite_table,column,item,gui_table):
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
    widget.pack(side=location, fill=BOTH, expand=1)
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

def edit_selection_view(sqlite_table,gui_table):
    item_values = gui_table.item(gui_table.selection())['values']
    if item_values:
        edit_view = Toplevel(window)
        window_height = 0
        for index,description in enumerate(gui_table.columns):
            if (description.lower() != 'type'):
                Label(edit_view,text=description).grid(row=index,column=0)
                Label(edit_view,text=item_values[index],foreground='blue').grid(row=index,column=1)
                if description.lower() == 'total':
                    total_text = StringVar()
                    total_entry = Entry(edit_view,textvariable=total_text)
                    total_entry.config(state="readonly")
                    total_entry.grid(row=index,column=2)
                else:
                    Entry(edit_view).grid(row=index, column=2)
                window_height += 35
                if (description.lower().find('date') != -1):  #add calendar selection widget for date entry
                    date_index = index
                    date_entry = edit_view.grid_slaves(row=date_index,column=2)[0]
                    date_entry.config(state="readonly")
                    def cal_button():
                        top = Toplevel(window)
                        cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                                       cursor="hand2")
                        cal.pack(fill="both", expand=True)
                        def retrieve_date():
                            date_entry.config(state=NORMAL)
                            date_entry.delete(0,END)
                            date_entry.insert(END,cal.selection_get().strftime('%Y-%m-%d'))
                            date_entry.config(state="readonly")
                            top.destroy()
                        Button(top, text="ok", command = retrieve_date).pack() #insert date into date entry
                        top.focus()
                    image = Image.open("calendar.png")
                    image = image.resize((22,22))
                    photo = ImageTk.PhotoImage(image)
                    cal_link = Button(edit_view,image=photo,command=cal_button)
                    cal_link.image = photo
                    cal_link.grid(row=index,column=3)
                elif (description.lower().find('total') != -1): #configure total entry to auto-update
                        entries = [x for x in reversed(edit_view.grid_slaves(column=0)) if (x.winfo_class() == 'Label' or x.winfo_class() == 'Menubutton')]
                        for entry in entries:
                            if entry.cget("text").lower() == "amount":
                                amount_row = entry.grid_info()['row']
                                amount_entry = edit_view.grid_slaves(row=amount_row,column=2)[0]
                            if entry.cget("text").lower() == "price":
                                price_row = entry.grid_info()['row']
                                price_entry = edit_view.grid_slaves(row=price_row,column=2)[0]
                        def total_after():
                            price_num = price_entry.get()
                            amount_num = amount_entry.get()
                            def total_update():
                                try:
                                    total_string = "$%.2f" % (float(amount_num)*float(price_num))
                                    total_text.set(total_string)
                                    return
                                except:
                                    total_string = "$"
                                    total_text.set(total_string)
                            total_update()
                            edit_view.after(150,total_after)
                        total_after()
            else:   #handle type case
                Label(edit_view,text=description).grid(row=index,column=0)
                Label(edit_view,text=item_values[index],foreground='blue').grid(row=index,column=1)
                global edit_var
                edit_var = StringVar(window)
                edit_var.set(type_options[sqlite_table][0])
                options = OptionMenu(edit_view,edit_var,*tuple(type_options[sqlite_table]))
                options.config(width=14, background = "white")
                options.grid(row=index, column=2)
                window_height += 35
        grid_size = edit_view.grid_size()[1] #used to place add/cancel buttons below all other buttons
        Button(edit_view,text="Edit Item",command = lambda: edit_selection(sqlite_table,edit_view)).grid(row=grid_size+1,column=2,sticky=N+E+S+W)
        Button(edit_view,text="Cancel",command = lambda: edit_view.destroy()).grid(row=grid_size+2,column=2,sticky=N+E+S+W)
        edit_view.title("Edit " + sqlite_table.replace("_"," "))
        edit_view.focus()
        x = (screen_width/2) - (500/2)
        y = (screen_height/2) - (500/2)
        edit_view.geometry("%dx%d+%d+%d" % (300,window_height,x,y))
        edit_view.resizable(0,0)
    else:
        messagebox.showerror("Selection Error","Please select an inventory item.")
        return

def edit_selection(sqlite_table,toplevel_widg):
    changes = []
    edit_entries = [x for x in reversed(toplevel_widg.grid_slaves()) if (x.winfo_class() == 'Entry' or x.winfo_class() == 'Menubutton')]
    for entry in edit_entries:
        if entry.winfo_class() == 'Entry' and entry.get():
            changes.append(' '.join(word[0].upper() + word[1:] for word in entry.get().split())) #titlecase the string before appending
        elif entry.winfo_class() == 'Menubutton':
            changes.append(edit_var.get())
        else:
            messagebox.showerror("Input Error","At least one input is blank, please try again.",parent=toplevel_widg)
            return
    current_values = [x.cget('text') for x in reversed(toplevel_widg.grid_slaves(column=1)) if (x.winfo_class() == 'Label')]
    changes = tuple(changes + current_values)
    raw_edit(changes)
    db_update()
    toplevel_widg.destroy()

#iterates through list of items and creates buttons based on 'class_name' object
def button_maker(class_name,list,master_widget,sqlite_table,gui_table):
    for item in list:
        class_name(master=master_widget,text=item,sqlite_table=sqlite_table,gui_table=gui_table).pack(anchor='center')

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
def add_item_view(sqlite_table,gui_table):
    window_height = 0
    add_view = Toplevel(window)
    for index,description in enumerate(gui_table.columns): #add labels and entries based on database labels
        if (description.lower() != 'type'):
            Label(add_view,text=description).grid(row=index,column=0)
            if description.lower() == 'total':
                total_text = StringVar()
                total_entry = Entry(add_view,textvariable=total_text)
                total_entry.config(state="readonly")
                total_entry.grid(row=index,column=1)
            elif (description.lower().find('age') != -1):
                age_text = StringVar()
                age_entry = Entry(add_view,textvariable=age_text)
                age_entry.config(state="readonly")
                age_entry.grid(row=index,column=1)
            else:
                Entry(add_view).grid(row=index, column=1)
            window_height += 35
            if (description.lower().find('date') != -1):  #add calendar selection widget for date entry
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
                        date_entry.insert(END,cal.selection_get().strftime('%Y-%m-%d'))
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
            elif ((description.lower().find('total') != -1) or (description.lower().find('age') != -1)): #configure total entry to auto-update
                    entries = [x for x in reversed(add_view.grid_slaves(column=0)) if (x.winfo_class() == 'Label' or x.winfo_class() == 'Menubutton')]
                    for entry in entries:
                        if entry.cget("text").lower() == "amount":
                            amount_row = entry.grid_info()['row']
                            amount_entry = add_view.grid_slaves(row=amount_row,column=1)[0]
                        if entry.cget("text").lower() == "price":
                            price_row = entry.grid_info()['row']
                            price_entry = add_view.grid_slaves(row=price_row,column=1)[0]
                        if (entry.cget("text").find("date") != -1):
                            date_row = entry.grid_info()['row']
                            date_entry = add_view.grid_slaves(row=date_row,column=1)[0]
                    def total_after():
                        def total_update():
                            if 'total_text' in locals():
                                try:
                                    price_num = price_entry.get()
                                    amount_num = amount_entry.get()
                                    total_string = "$%.2f" % (float(amount_num)*float(price_num))
                                    total_text.set(total_string)
                                    return
                                except:
                                    total_string = "$"
                                    total_text.set(total_string)
                            if 'age_text' in locals():
                                try:
                                    date_value = datetime.strptime(date_entry.get(),'%Y-%m-%d')
                                    date_diff = datetime.now() - date_value
                                    age_value = "%d years, %d months" % (math.floor(date_diff.days/365.2425), (date_diff.days%365.2425)/30)
                                    age_text.set(age_value)
                                except:
                                    age_text.set("0 years, 0 months")
                        total_update()
                        add_view.after(150,total_after)
                    total_after()
        else:   #handle type case
            Label(add_view,text=description).grid(row=index,column=0)
            global type_var
            type_var = StringVar(window)
            type_var.set(type_options[sqlite_table][0])
            options = OptionMenu(add_view,type_var,*tuple(type_options[sqlite_table]))
            options.config(width=14, background = "white")
            options.grid(row=index, column=1)
            window_height += 35
    grid_size = add_view.grid_size()[1] #used to place add/cancel buttons below all other buttons
    Button(add_view,text="Add Item",command = lambda: add_item(sqlite_table,add_view)).grid(row=grid_size+1,column=1,sticky=N+E+S+W)
    Button(add_view,text="Cancel",command = lambda: add_view.destroy()).grid(row=grid_size+2,column=1,sticky=N+E+S+W)
    add_view.title("Add to " + sqlite_table.replace("_"," "))
    add_view.focus()
    x = (screen_width/2) - (500/2)
    y = (screen_height/2) - (500/2)
    add_view.geometry("%dx%d+%d+%d" % (300,window_height,x,y))
    add_view.resizable(0,0)

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
        if entry.winfo_class() == 'Entry' and entry.get():
            additions.append(' '.join(word[0].upper() + word[1:] for word in entry.get().split())) #titlecase the string before appending
            num_entries += 1
        elif entry.winfo_class() == 'Menubutton':
            additions.append(type_var.get())
            num_entries += 1
        else:
            messagebox.showerror("Input Error","At least one input is blank, please try again.",parent=toplevel_widg)
            return
    additions = tuple(additions)
    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("INSERT INTO \'" + sqlite_table + "\' VALUES (" + ("?,"*(num_entries-1)) + "?)", additions)
    conn.commit()
    conn.close()
    db_update()
    toplevel_widg.destroy()

def treeview_sort_column(tv, col, reverse):
    l = [(tv.set(k, col), k) for k in tv.get_children('')]
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        tv.move(k, '', index)
        tv.item(k,tags=())
        if index % 2 == 0:
            tv.item(k,tags=('even',))
    tv.tag_configure('even',background="#E8E8E8")

    # reverse sort next time
    tv.heading(col, text=col, command=lambda c=col: treeview_sort_column(tv, c, not reverse))

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
        Button.__init__(self,master,text=text,command = lambda: view_products(sqlite_table,"Type",text,gui_table),width=20,height=2, font=('Calibri',12,'bold'))

#gives production buttons functionality
class Inventory_Button(Button):
    def __init__(self,master,text,sqlite_table,gui_table):
        self.sqlite_table = sqlite_table
        self.gui_table = gui_table
        Button.__init__(self,master,text=text,width=20,height=2,font=('Calibri',12,'bold'))

class Logistics_Button(Button):
    def __init__(self,master,text,sqlite_table,gui_table,command):
        self.sqlite_table = sqlite_table
        self.gui_table = gui_table
        Button.__init__(self,master=master,text=text,width=20,height=2,font=('Calibri',12,'bold'),command=command)
        self.pack(anchor='center')

class Treeview_Table(ttk.Treeview):

    def __init__(self,master,columns):
        ttk.Treeview.__init__(self,master,columns=columns,show='headings',height=600,style="Custom.Treeview")
        self.width=int(table_width/(len(columns)))
        self.columns = columns
        for i in range(len(columns)):
            self.column(self.columns[i],anchor='center',width=self.width)
            self.heading(str('#' + str((i+1))),text=self.columns[i],command = lambda col=self.columns[i]: treeview_sort_column(self,col, False))
        self.pack(side=RIGHT,fill=BOTH,expand=1)

#used to search for the string literal within a filename that occurs before the file extension (Ex. '.txt')
fileRegex = re.compile(r'''
    ([a-zA-Z0-9_ -]+)
    (.)
    ([a-zA-Z_0-9])''',re.VERBOSE)

#option values for dropdown menus
type_options = {'raw_materials': ['Bottles','Boxes','Caps','Capsules','Labels'], 'bottles': ['Vodka','Whiskey','Rum','Other'], 'barrels': ['Bourbon','Rye','Malt','Rum','Other'], 'grain': ['Corn','Rye','Malted Barley','Malted Wheat','Oat']}

#create root window, resize based on user's screen info
window = Tk()
window.title("Albany Distilling Company Inventory")
screen_width = window.winfo_screenwidth()
screen_height = window.winfo_screenheight()
width = int(screen_width/1.5)
height = int(screen_height/1.5)
command_width = int(.33*width)
table_width = int(.66*width)
x = (screen_width/2) - (width/2)
y = ((screen_height/2) - (height/2)) - 50
window.geometry("%dx%d+%d+%d" % (width,height,x,y))
window.resizable(1,1)

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
s.configure("Treeview.Heading", font=('Calibri', 12,'bold'))
s.configure("TButton",font=('Calibri',12,'bold'))

#create/load and display database
inventory = database()

#create bottle inventory notebook, populate with tabbed frames
bottle_inventory_notebook = ttk.Notebook(window, height=height, width=width)
raw_materials_frame = ttk.Frame(bottle_inventory_notebook)
bottle_frame = ttk.Frame(bottle_inventory_notebook)
production_frame = ttk.Frame(bottle_inventory_notebook)
materials_used_frame = ttk.Frame(bottle_inventory_notebook)
bottle_inventory_notebook.add(raw_materials_frame, text = "Raw Materials",padding=10)
bottle_inventory_notebook.add(production_frame, text="Production Log",padding=10)
bottle_inventory_notebook.add(materials_used_frame, text="Materials Used", padding=10)
bottle_inventory_notebook.add(bottle_frame, text = "Bottle Inventory",padding=10)
bottle_inventory_notebook.pack(side=BOTTOM,fill=BOTH,expand=1)

#create raw materials table
raw_materials_table = Treeview_Table(raw_materials_frame,("Type","Item","Amount","Price","Total"))

#show table upon opening application
view_products('raw_materials','null','All',raw_materials_table)

#create raw materials command frame and populate with view and options buttons
raw_materials_command_frame = Frame(raw_materials_frame, height = height,width = command_width)

raw_materials_view_frame = LabelFrame(raw_materials_command_frame,height = height, bd = 5, relief= RIDGE, text="View", font="bold")
raw_materials_view_buttons = ["Bottles","Boxes","Caps","Capsules","Labels","All"]
button_maker(View_Button,raw_materials_view_buttons,raw_materials_view_frame,'raw_materials',raw_materials_table)

raw_materials_option_frame = LabelFrame(raw_materials_command_frame,height = height, text = "Options", bd = 5, relief = RIDGE, font = "bold")
Logistics_Button(raw_materials_option_frame,"Add Item",'raw_materials',raw_materials_table,lambda: add_item_view('raw_materials',raw_materials_table))
Logistics_Button(raw_materials_option_frame,"Edit Selection",'raw_materials',raw_materials_table,lambda: edit_selection_view('raw_materials',raw_materials_table))

raw_materials_view_frame.pack()
raw_materials_option_frame.pack()
raw_materials_command_frame.pack(padx=10)

#create production table
production_table = Treeview_Table(production_frame,("Date","Product","Amount"))

#TODO: populate production table with production database info

#create production commands frame and populate with an edit button
production_command_frame = Frame(production_frame,height=height,width=command_width)

production_opt_frame = LabelFrame(production_command_frame,height=height,bd=5,relief=RIDGE,text="Options",font="bold")
Logistics_Button(production_opt_frame,"Edit Selection",'production',production_table,None)

production_opt_frame.pack()
production_command_frame.pack(padx=10)

#create materials used table
materials_used_table = Treeview_Table(materials_used_frame,("Product", "Amount","Date"))

#TODO: populate materials used table

#create bottle table
bottle_table = Treeview_Table(bottle_frame,("Type","Product","Amount","Price","Total"))

#create bottle command frame and populate with view and option buttons
bottle_command_frame = Frame(bottle_frame,height=height,width=command_width)

bottle_view_frame = LabelFrame(bottle_command_frame,height=height, bd=5, relief=RIDGE, text="View", font="bold")
bottle_view_buttons = ["Vodka","Whiskey","Rum","Other","All"]
button_maker(View_Button,bottle_view_buttons,bottle_view_frame,'bottles',bottle_table)

bottle_option_frame = LabelFrame(bottle_command_frame, height=height, bd=5, relief=RIDGE, text="Options", font="bold")
Logistics_Button(bottle_option_frame,"Add Item",'bottles',bottle_table,lambda: add_item_view('bottles',bottle_table))

bottle_view_frame.pack()
bottle_option_frame.pack()
bottle_command_frame.pack(padx=10)

#create grain inventory notebook, populate with tabbed frames
grain_inventory_notebook = ttk.Notebook(window, height=height, width=width)
grain_inventory_frame = ttk.Frame(grain_inventory_notebook)
grain_inventory_notebook.add(grain_inventory_frame, text="Grain Inventory", padding=10)

#create grain inventory table and pack within grain frame
grain_table = Treeview_Table(grain_inventory_frame,("Order No.","Type","Amount","Price","Total"))

#create grain command frame and populate with option buttons
grain_command_frame = Frame(grain_inventory_frame,height=height,width=command_width)

grain_option_frame = LabelFrame(grain_command_frame,height=height,bd=5,relief=RIDGE,text="Options",font="bold")
Logistics_Button(grain_option_frame,"Produce Mash",'grain',grain_table,None)
Logistics_Button(grain_option_frame,"Edit Selection",'grain',grain_table,None)
Logistics_Button(grain_option_frame,"Mash Production Sheet",'grain',grain_table,None)
Logistics_Button(grain_option_frame,"Add Grain",'grain',grain_table,lambda: add_item_view('grain',grain_table))

grain_option_frame.pack()
grain_command_frame.pack(padx=10)

#create barrel inventory notebook and populates with tabbed frames
barrel_inventory_notebook = ttk.Notebook(window, height=height, width=width)
barrel_frame = ttk.Frame(barrel_inventory_notebook)
barrel_inventory_notebook.add(barrel_frame, text="Barrel Inventory",padding=10)

#create barrel inventory table
barrel_table = Treeview_Table(barrel_frame,("Barrel No.","Type","Proof Gallons","Date Filled","Age","Investor"))

#create barrel command frame and populate with view and option buttons
barrel_command_frame = Frame(barrel_frame,height=height,width=command_width)

barrel_view_frame = LabelFrame(barrel_command_frame,height=height,bd=5,relief=RIDGE,text="View",font="bold")
barrel_view_buttons = ["Bourbon","Rye","Malt","Other","All"]
button_maker(View_Button,barrel_view_buttons,barrel_view_frame,'barrels',barrel_table)

barrel_option_frame = LabelFrame(barrel_command_frame,height=height,bd=5,relief=RIDGE,text="Options",font="bold")
Logistics_Button(barrel_option_frame,"Add Barrel",'barrels',barrel_table,lambda: add_item_view('barrels',barrel_table))

barrel_view_frame.pack()
barrel_option_frame.pack()
barrel_command_frame.pack(padx=10)

#create purchase orders notebook with tabbed frames
purchase_orders_notebook = ttk.Notebook(window,height=height,width=width)
purchase_orders_frame = Frame(purchase_orders_notebook)
purchase_orders_notebook.add(purchase_orders_frame,text="Purchase Orders",padding=10)

#create purchase orders table
purchase_orders_table = Treeview_Table(purchase_orders_frame,("Date","Product","Amount","Price","Total","Destination","PO No."))

#create purchase orders command frame and populate with option buttons
purchase_orders_command_frame = Frame(purchase_orders_frame,height=height,width=command_width)

purchase_orders_option_frame = LabelFrame(purchase_orders_command_frame,height=height,bd=5,relief=RIDGE,text="Options",font='bold')
Logistics_Button(purchase_orders_option_frame,"Create Purchase Order",'purchase_orders',purchase_orders_table,None)
Logistics_Button(purchase_orders_option_frame,"View Purchase Order",'purchase_orders',purchase_orders_table,None)
Logistics_Button(purchase_orders_option_frame,"Edit Selection",'purchase_orders',purchase_orders_table,None)

purchase_orders_option_frame.pack()
purchase_orders_command_frame.pack(padx=10)

#create employee transactions notebook and populate with tabbed frames
employee_transactions_notebook = ttk.Notebook(window,height=height,width=width)
employee_transactions_frame = Frame(employee_transactions_notebook)
employee_transactions_notebook.add(employee_transactions_frame,text="Employee Transactions",padding=10)

#create employee transactions table
employee_transactions_table = Treeview_Table(employee_transactions_frame,("Date","Product","Amount","Employee"))

#create employee transactions command frame and populate with option buttons
employee_transactions_command_frame = Frame(employee_transactions_frame,height=height,width=command_width)

employee_transactions_options_frame = LabelFrame(employee_transactions_command_frame,height=height,bd=5,relief=RIDGE,text="Options",font="bold")
Logistics_Button(employee_transactions_options_frame,"Checkout Bottles",'employee_transactions',employee_transactions_table,None)
Logistics_Button(employee_transactions_options_frame,"Edit Selection",'employee_transactions',employee_transactions_table,None)

employee_transactions_options_frame.pack()
employee_transactions_command_frame.pack(padx=10)

#create menu bar at the top of the gui, populate with clickable tabs
menubar = Menu(window)

menu1 = Menu(menubar, tearoff=0)
menu1.add_command(label="Raw Materials and Bottles", command=lambda: view_widget(window,bottle_inventory_notebook,BOTTOM,'raw_materials','null','All',raw_materials_table))
menu1.add_command(label="Grain", command=lambda: view_widget(window,grain_inventory_notebook,BOTTOM,'grain','null','All',grain_table))
menu1.add_command(label="Barrels", command=lambda: view_widget(window,barrel_inventory_notebook,BOTTOM,'barrels','null','All',barrel_table))
menubar.add_cascade(label="Inventory", menu=menu1)

menu2 = Menu(menubar, tearoff=0)
menu2.add_command(label="Purchase Orders", command=lambda: view_widget(window,purchase_orders_notebook,BOTTOM,'purchase_orders','null','All',purchase_orders_table))
menu2.add_command(label="Employee Transactions", command=lambda: view_widget(window,employee_transactions_notebook,BOTTOM,'employee_transactions','null','All',employee_transactions_table))
menubar.add_cascade(label="Shipping and Transactions",menu=menu2)

menu3 = Menu(menubar, tearoff=0)
menu3.add_command(label="Production Sheets", command=sheets_view)
menu3.add_command(label="Case Labels", command=labels_view)
menubar.add_cascade(label="Files", menu=menu3)

window.config(menu=menubar)
window.mainloop()
