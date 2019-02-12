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
    """Create inventory database if it does not exist. Update certain values within
    the database.
    """

    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS 'raw_materials' (type TEXT, product TEXT, amount INTEGER, price REAL, total TEXT)")
    cur.execute("UPDATE 'raw_materials' SET total=PRINTF('%s%.2f', '$', amount*price)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'production' (date DATE, product TEXT, amount INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'in_progress' (date DATE, product TEXT, amount INTEGER, case_size INTEGER)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'bottles' (type TEXT, product TEXT, cases INTEGER, case_size INTEGER, price REAL, total TEXT)")
    cur.execute("UPDATE 'bottles' SET total=PRINTF('%s%.2f', '$', cases*price)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'samples' (type TEXT, product TEXT, amount INTEGER, price REAL, total TEXT)")
    cur.execute("UPDATE 'samples' SET total=PRINTF('%s%.2f', '$', amount*price)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'grain' ('order_number' TEXT, type TEXT, amount INTEGER,price REAL, total TEXT)")
    cur.execute("UPDATE 'grain' SET total=PRINTF('%s%.2f', '$', amount*price)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'barrels' ('barrel_number' TEXT, type TEXT,'pg' INTEGER, 'date_filled' DATE, age TEXT,investor TEXT)")
    cur.execute("UPDATE 'barrels' SET age=PRINTF('%d years, %d months',(julianday('now') - julianday(date_filled)) / 365,(julianday('now') - julianday(date_filled)) % 365 / 30)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'purchase_orders' (date DATE,product TEXT, amount INTEGER, price REAL, total REAL, destination TEXT, 'po_number' TEXT)")
    cur.execute("CREATE TABLE IF NOT EXISTS 'employee_transactions' (date DATE,product TEXT, amount INTEGER, employee TEXT)")
    conn.commit()
    conn.close()

def db_update():
    """Updates inventory database values for "total" column in raw_materials,bottles,
    and grain tables. Updates "age" values for the barrels table.
    """

    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("UPDATE 'raw_materials' SET total=PRINTF('%s%g', '$', amount*price)")
    cur.execute("UPDATE 'bottles' SET total=PRINTF('%s%g', '$', cases*price)")
    cur.execute("UPDATE 'samples' SET total=PRINTF('%s%.2f', '$', amount*price)")
    cur.execute("UPDATE 'grain' SET total=PRINTF('%s%g', '$', amount*price)")
    cur.execute("UPDATE 'barrels' SET age=PRINTF('%d years, %d months',(julianday('now') - julianday(date_filled)) / 365,(julianday('now') - julianday(date_filled)) % 365 / 30)")
    conn.commit()
    conn.close()

def raw_edit(sql_edit):
    """Updates the 'raw_materials' table with the changes provided by sql_edit.

    Args:
        sql_edit (tuple):Contains the changes and current values for updating the table row.
    """

    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("UPDATE 'raw_materials' SET type=?,product=?,amount=?,price=?,total=? WHERE type=? AND product=? AND amount=? AND price=? AND total=?", sql_edit)
    conn.commit()
    conn.close()

def production_edit(sql_edit):
    """Updates the 'production' table with changes provided by sql_edit.

    Args:
        sql_edit (tuple):Contains the changes and current values for updating the table row
    """

    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("UPDATE 'production' SET date=?, product=?, amount=? WHERE date=? AND product=? AND amount=?", sql_edit)
    conn.commit()
    conn.close()

def in_progress_edit(sql_edit):
    """Updates the 'in_progress' table with changes provided by sql_edit.

    Args:
        sql_edit (tuple):Contains the changes and current values for updating the table row
    """

    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("UPDATE 'in_progress' SET date=?, product=?, amount=?, case_size=? WHERE date=? AND product=? AND amount=? AND case_size=?", sql_edit)
    conn.commit()
    conn.close()

def bottles_edit(sql_edit):
    """Updates 'bottles' table with changes provided by sql_edit.

    Args:
        sql_edit (tuple):Contains the changes and current values for updating the table row
    """

    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("UPDATE 'bottles' SET type=?, product=?, cases=?, case_size=?, price=?, total=? WHERE type=? AND product=? AND cases=? AND case_size=? AND price=? AND total=?", sql_edit)
    conn.commit()
    conn.close()

def sample_edit(sql_edit):
    """Updates 'samples' table with changes provided by sql_edit.

    Args:
        sql_edit (tuple):Contains the changes and current values for updating the table row
    """

    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("UPDATE 'samples' SET type=?, product=?, amount=?, price=?, total=? WHERE type=? AND product=? AND amount=? AND price=? AND total=?", sql_edit)
    conn.commit()
    conn.close()

def barrel_edit(sql_edit):
    """Updates the 'barrels' table with the changes provided by sql_edit.

    Args:
        sql_edit (tuple):Contains the changes and current values for updating the table row.
    """

    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("UPDATE 'barrels' SET barrel_number=?,type=?,pg=?,date_filled=?,age=?,investor=? WHERE barrel_number=? AND type=? AND pg=? AND date_filled=? AND age=? AND investor=?", sql_edit)
    conn.commit()
    conn.close()

def grain_edit(sql_edit):
    """Updates the 'grain' table with the changes provided by sql_edit.

    Args:
        sql_edit (tuple):Contains the changes and current values for updating the table row.
    """

    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("UPDATE 'grain' SET order_number=?,type=?,amount=?,price=?,total=? WHERE order_number=? AND type=? AND amount=? AND price=? AND total=?", sql_edit)
    conn.commit()
    conn.close()

def view_widget(window,widget,location,sqlite_table,column,item,gui_table):
    """Removes current packed widgets from window frame and replaces with new widget
    chosen.

    Args:
        window (Tk root object):Master window to remove widgets from
        widget (Tk widget object):Widget to be displayed
        location (str):Position to pack new widget
        sqlite_table (sqlite table):Table to display information from
        column (str):Column to which the 'item' filter is applied
        item (str):Item which is filtered for
        gui_table (Tk treeview object):Table where info will be displayed
    Returns:
        view_products(sqlite_table,column,item,gui_table)
    """

    for widg in window.pack_slaves():
        widg.pack_forget()
    widget.pack(side=location, fill=BOTH, expand=1)
    view_products(sqlite_table,column,item,gui_table)

def view_products(sqlite_table,column,item,gui_table):
    """Fetches info from sqlite_table based on an item filter. Returns information
    into the current gui_table.Configures even-numbered rows to have a grey background.

    Args:
        sqlite_table(str):Sqlite table to fetch data from.
        column (str):Column to which the 'item' filter is applied
        item (str):Item which is filtered for.
        gui_table (Tk treeview object):Table where info will be displayed.
    """

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

def sheets_view():
    """Displays a toplevel window populated by clickable links to production sheets.
    Production sheets are found within the 'production_sheets' folder.
    """

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

def labels_view():
    """Displays a toplevel window populated by clickable links to case label sheets.
    Label sheets are found within the 'case_labels' folder.
    """

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


def edit_check(sqlite_table,gui_table,edit_func):
    """Checks current gui_table to see if a selection has been made. If so, creates
    an instance of the Edit_View class, creating a populated toplevel window. If not,
    displays a messagebox prompting the user to make a selection.

    Args:
        sqlite_table (sqlite table):Used as Edit_View arg. See Edit_View for details.
        gui_table (Tk treeview table):Used as Edit_View arg. See Edit_View for details.
        edit_func (function):Used as Edit_View arg. See Edit_View for details.
    Returns:
        Edit_View(window,sqlite_table,gui_table,2,edit_func)
    """

    item_values = gui_table.item(gui_table.selection())['values']
    if item_values:
        Edit_View(window,sqlite_table,gui_table,2,edit_func)
    else:
        messagebox.showerror("Selection Error","Please select an inventory item.")

def gui_table_sort(gui_table, column, reverse):
    """Sorts gui tables in ascending order based on the column header clicked.
    The next click upon the header will be in reverse order.

    Args:
        gui_table (Tk treeview table):Table that will be sorted
        column (str):Column name used as basis for sorting
        reverse (bool):Whether or not the sort is in reverse
    """
    l = [(gui_table.set(k, column), k) for k in gui_table.get_children()]
    print(gui_table.get_children(''))
    l.sort(reverse=reverse)

    # rearrange items in sorted positions
    for index, (val, k) in enumerate(l):
        gui_table.move(k, '', index)
        gui_table.item(k,tags=())
        if index % 2 == 0:
            gui_table.item(k,tags=('even',))
    gui_table.tag_configure('even',background="#E8E8E8")

    # reverse sort next time
    gui_table.heading(column, text=column, command=lambda c=column: gui_table_sort(gui_table, c, not reverse))

def total_update(sqlite_table):
    """Returns the sum of all values in a table's total column. Used by the
    Total_Label class to display the output.

    Args:
        sqlite_table (sqlite table):Table from which total values are taken
    Returns:
        total, where total = SUM(amount*price) from the sqlite table
    """
    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("SELECT SUM(amount*price) FROM " + sqlite_table)
    total = list(cur)[0][0]
    conn.close()
    return total

#creates toplevel populated by inputs for items in table
class Add_View(Toplevel):
    """A toplevel widget with labels corresponding to sqlite table columns and entry
    widgets to insert data into the table.

    Args:
        master (tkinter widget object):Parent widget of the Add_View object
        sqlite_table (sqlite table):Table that will be added to
        gui_table (Tk treeview table):Table where label and entry widgets will come
            from
        entry_col (int):Column index where entries will be placed by .grid()
    """

    def __init__(self,master,sqlite_table,gui_table,entry_col):
        self.window_height = 0
        self.sqlite_table = sqlite_table
        self.gui_table = gui_table
        self.entry_col = entry_col
        self.x = (screen_width/2) - (width/2) + 100
        self.y = ((screen_height/2) - (height/2)) + 50
        Toplevel.__init__(self,master=master)
        self.title_frame = Frame(self)
        Label(self.title_frame,text="Add Product to "+ self.sqlite_table.replace("_"," ").title() + " Inventory",font="Arial 10 bold").pack()
        self.title_frame.grid(row=0,column=0,columnspan=2)
        for index,description in enumerate(self.gui_table.columns,1):
            if (description.lower() != 'type'):
                Label(self,text=description + ":").grid(row=index,column=0,sticky=W)
                if description.lower() == 'total':
                    self.total_text = StringVar()
                    self.total_entry = Entry(self,textvariable=self.total_text)
                    self.total_entry.config(state="readonly")
                    self.total_entry.grid(row=index,column=self.entry_col)
                elif (description.lower().find('age') != -1):
                    self.age_text = StringVar()
                    self.age_entry = Entry(self, textvariable=self.age_text)
                    self.age_entry.config(state="readonly")
                    self.age_entry.grid(row=index,column=self.entry_col)
                else:
                    Entry(self).grid(row=index,column=self.entry_col)
                self.window_height += 35
                if (description.lower().find('date') != -1):
                    self.date_index = index
                    self.date_entry = self.grid_slaves(row=self.date_index,column=self.entry_col)[0]
                    self.date_entry.config(state="readonly")
                    self.image = Image.open("calendar.png")
                    self.image = self.image.resize((22,22))
                    self.photo = ImageTk.PhotoImage(self.image)
                    self.cal_link = Button(self, image=self.photo, command = self.cal_button)
                    self.cal_link.image = self.photo
                    self.cal_link.grid(row=index,column=self.entry_col+1)
                elif ((description.lower().find('total') != -1) or (description.lower().find('age') != -1)):
                    self.labels = [x for x in reversed(self.grid_slaves(column=0)) if (x.winfo_class() == 'Label')]
                    for entry in self.labels:
                        if entry.cget("text").lower().find("amount") != -1:
                            self.amount_row = entry.grid_info()['row']
                            self.amount_entry = self.grid_slaves(row=self.amount_row,column=self.entry_col)[0]
                        if entry.cget("text").lower().find("price") != -1:
                            self.price_row = entry.grid_info()['row']
                            self.price_entry = self.grid_slaves(row=self.price_row,column=self.entry_col)[0]
                    self.total_after()
            else:   #handle type case
                Label(self,text=description + ":").grid(row=index,column=0,sticky=W)
                self.type_var = StringVar(master)
                self.type_var.set(type_options[sqlite_table][0])
                self.options = OptionMenu(self,self.type_var,*tuple(type_options[sqlite_table]))
                self.options.config(width=14, background="white")
                self.options.grid(row=index,column=self.entry_col)
                self.window_height += 35
        self.grid_size = self.grid_size()[1]
        self.button_frame = Frame(self)
        Button(self.button_frame,text="Add Item",width=10,command = lambda : self.add_item(self.sqlite_table)).pack(side=LEFT,padx=5,pady=5)
        Button(self.button_frame,text="Cancel",width=10,command = lambda : self.destroy()).pack(side=LEFT,padx=5,pady=5)
        self.button_frame.grid(row=self.grid_size+1,column=0,columnspan=2)
        self.title("Add to " + self.sqlite_table.replace("_"," ").title())
        self.focus()
        self.geometry("+%d+%d" % (self.x,self.y))
        self.resizable(0,0)

    def add_item(self,sqlite_table):
        '''Work through Add_View toplevel to find entry widgets and extract these values to be
        inserted into the given sqlite table. Uses db_update() to update certain
        column values afterwards and view_products() to display the updated gui table.

        Args:
            sqlite_table (sqlite table):Table to insert new entry within
        Returns:
            db_update()
            view_products(self.sqlite_table,'null','All',self.gui_table)
        '''

        self.additions = []
        self.num_entries = 0
        self.entries = [x for x in reversed(self.grid_slaves()) if (x.winfo_class() == 'Entry' or x.winfo_class() == 'Menubutton')]
        for entry in self.entries: #work through add_item entry widgets
            if entry.winfo_class() == 'Entry' and entry.get():
                self.additions.append(' '.join(word[0].upper() + word[1:] for word in entry.get().split())) #titlecase the string before appending
                self.num_entries += 1
            elif entry.winfo_class() == 'Menubutton':
                self.additions.append(self.type_var.get())
                self.num_entries += 1
            else:
                messagebox.showerror("Input Error","At least one input is blank, please try again.",parent=self)
                return
        self.additions = tuple(self.additions)
        self.conn = sqlite3.Connection("inventory.db")
        self.cur = self.conn.cursor()
        self.cur.execute("INSERT INTO \'" + self.sqlite_table + "\' VALUES (" + ("?,"*(self.num_entries-1)) + "?)", self.additions)
        self.conn.commit()
        self.conn.close()
        db_update()
        view_products(self.sqlite_table,'null','All',self.gui_table)
        self.destroy()

    def cal_button(self):
        """Creates a toplevel window to provide a calendar date selection tool.
        """

        self.top = Toplevel(window)
        self.cal = Calendar(self.top, font="Arial 14", selectmode='day', locale='en_US',
                       cursor="hand2")
        self.cal.pack(fill="both", expand=True)
        def retrieve_date():
            """Updates the date-entry widget within the toplevel widget.
            """
            self.date_entry.config(state=NORMAL)
            self.date_entry.delete(0,END)
            self.date_entry.insert(END,self.cal.selection_get().strftime("%Y-%m-%d"))
            self.date_entry.config(state="readonly")
            self.top.destroy()
        Button(self.top, text="ok", command = retrieve_date).pack()
        self.top.focus()

    def total_after(self):
        """Widget after-function to auto-update total and age entry values.Repeats
        every 150ms.
        """
        def total_update():
            """Tries to update total and age entry values.

            Raises:
                AttributeError: if price_entry, amount_entry or date_entry don't exist
                ValueError: if price_entry, amount_entry or date_entry values are
                    currently empty
            """

            try:
                self.price_num = self.price_entry.get()
                self.amount_num = self.amount_entry.get()
                self.total_string = "$%.2f" % (float(self.amount_num)*float(self.price_num))
                self.total_text.set(self.total_string)
                return
            except (AttributeError, ValueError):
                pass
            try:
                self.date_value = datetime.strptime(self.date_entry.get(),'%Y-%m-%d')
                self.date_diff = datetime.now() - self.date_value
                self.barrel_age = "%d years, %d months" % (math.floor(self.date_diff.days/365.2425), (self.date_diff.days%365.2425)/30)
                self.age_text.set(self.barrel_age)
            except (AttributeError, ValueError):
                pass
        total_update()
        self.after(150,self.total_after)

class Edit_View(Add_View):

    def __init__(self,master,sqlite_table,gui_table,entry_col,edit_func):
        self.master = master
        self.sqlite_table = sqlite_table
        self.gui_table = gui_table
        self.entry_col = entry_col
        self.edit_func = edit_func
        self.item_values = self.gui_table.item(self.gui_table.selection())['values']
        if self.item_values:
            Add_View.__init__(self,master,sqlite_table,gui_table,entry_col)
            self.title("Edit " + self.sqlite_table.replace("_"," ").title())
            self.title_frame.destroy()
            self.title_frame = Frame(self)
            Label(self.title_frame,text="Edit Product in "+ self.sqlite_table.replace("_"," ").title() + " Inventory",font="Arial 10 bold").pack()
            self.title_frame.grid(row=0,column=0,columnspan=3)
            for index,description in enumerate(self.gui_table.columns):
                if (description.lower() != 'type'):
                    Label(self,text=self.item_values[index],foreground='blue').grid(row=index+1,column=1)
                else:
                    Label(self,text=self.item_values[index],foreground='blue').grid(row=index+1,column=1)
            self.button_frame.destroy()
            self.button_frame = Frame(self)
            Button(self.button_frame,text="Edit Item",command = lambda : self.edit_selection(self.edit_func)).pack(side=LEFT,padx=5,pady=5)
            Button(self.button_frame,text="Cancel",command = lambda : self.destroy()).pack(side=LEFT,padx=5,pady=5)
            self.button_frame.grid(row=self.grid_size+1,column=0,columnspan=3)

    def edit_selection(self,edit_func):
        self.changes = []
        self.edit_entries = [x for x in reversed(self.grid_slaves()) if (x.winfo_class() == 'Entry' or x.winfo_class() == 'Menubutton')]
        for entry in self.edit_entries:
            if entry.winfo_class() == 'Entry' and entry.get():
                self.changes.append(' '.join(word[0].upper() + word[1:] for word in entry.get().split())) #titlecase the string before appending
            elif entry.winfo_class() == 'Menubutton':
                self.changes.append(self.type_var.get())
            else:
                messagebox.showerror("Input Error","At least one input is blank, please try again.",parent=self)
                return
        self.current_values = [x.cget('text') for x in reversed(self.grid_slaves(column=1)) if (x.winfo_class() == 'Label')]
        self.changes = tuple(self.changes + self.current_values)
        edit_func(self.changes)
        db_update()
        view_products(self.sqlite_table,'null','All',self.gui_table)
        self.destroy()

class Production_View(Toplevel):

    def __init__(self,master,sqlite_table,gui_table):
        self.master = master
        self.sqlite_table = sqlite_table
        self.gui_table = gui_table
        self.x = (screen_width/2) - (width/2) + 100
        self.y = ((screen_height/2) - (height/2)) + 50
        Toplevel.__init__(self,master=master)
        conn = sqlite3.Connection("inventory.db")
        cur = conn.cursor()
        cur.execute("SELECT product FROM \'" + self.sqlite_table + "\'")
        product_rows = cur.fetchall()
        print(product_rows)
        product_list = [x[0] for x in product_rows]
        for index,description in enumerate(self.gui_table.columns):
            if (description.lower() == 'type'):
                Label(self,text=description + ":").grid(row=index,column=0,sticky=W)
                self.type_var = StringVar(master)
                self.type_var.set(type_options[sqlite_table][0])
                self.options = OptionMenu(self,self.type_var,*tuple(type_options[sqlite_table]))
                self.options.config(width=14, background="white")
                self.options.grid(row=index,column=1)
            if (description.lower() == 'product'):
                Label(self,text=description + ":").grid(row=index,column=0,sticky=W)
                self.product_var = StringVar(master)
                self.product_var.set(product_rows[0][0])
                self.products = OptionMenu(self,self.product_var,*tuple(product_list))
                self.products.grid(row=index,column=1)
        self.title("Production")
        self.focus()
        self.geometry("+%d+%d" % (self.x,self.y))
        self.resizable(0,0)


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

class Command_Frame(Frame):
    """Creates frame on the left side of the treeview tables. Used to place command
    buttons for interacting with data.

    Args:
        master (Tk widget object):Parent widget of the Command_Frame
    """

    def __init__(self,master):
        self.master = master
        self.height = height
        self.width = command_width
        Frame.__init__(self,master=self.master,height=self.height,width=self.width)

class View_Frame(LabelFrame):

    def __init__(self,master,sqlite_table,gui_table,labels):
        self.master = master
        self.sqlite_table = sqlite_table
        self.gui_table = gui_table
        self.height = int(screen_height/1.5)
        self.labels = labels
        LabelFrame.__init__(self,master=self.master,height=self.height,bd=5,relief=RIDGE,text="View",font="bold")
        for label in self.labels:
            View_Button(master=self,text=label,sqlite_table=self.sqlite_table,gui_table=self.gui_table)
        self.pack()

class Option_Frame(LabelFrame):

    def __init__(self,master):
        self.master = master
        self.height = height
        LabelFrame.__init__(self,master=self.master,text="Options",height=self.height,relief=RIDGE,font="bold",bd=5)

#gives view button functionality to view items by type
class View_Button(Button):

    def __init__(self,master,text,sqlite_table,gui_table):
        self.sqlite_table = sqlite_table
        self.gui_table = gui_table
        Button.__init__(self,master,text=text,command = lambda: view_products(sqlite_table,"Type",text,gui_table),width=20,height=2, font=('Calibri',12,'bold'))
        self.pack()

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
            self.heading(str('#' + str((i+1))),text=self.columns[i],command = lambda col=self.columns[i]: gui_table_sort(self,col, False))
        self.pack(side=RIGHT,fill=BOTH,expand=1)

class Total_Label(LabelFrame):

    def __init__(self,sqlite_table,master):
        self.sqlite_table = sqlite_table
        self.master = master
        self.text_var = StringVar()
        LabelFrame.__init__(self,master,height=height,width=command_width,text="Inventory Value",bd=5,relief=RIDGE,font="bold")
        self.total_after()
        Label(self,textvariable=self.text_var,bd=10,font="Arial 15 bold",fg="dark slate grey").pack(fill=BOTH)
        self.pack(side=BOTTOM,fill=X)

    def total_after(self):
        try:
            self.text = "{0:,.2f}".format(total_update(self.sqlite_table))
            self.text_var.set("$%s" % (self.text))
        except:
            self.text_var.set("$0.00")
        self.after(150,self.total_after)

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
width = int(screen_width/1.2)
height = int(screen_height/1.2)
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
production_frame = ttk.Frame(bottle_inventory_notebook)
inprog_fr = ttk.Frame(bottle_inventory_notebook)
bottle_frame = ttk.Frame(bottle_inventory_notebook)
samples_frame = ttk.Frame(bottle_inventory_notebook)
bottle_inventory_notebook.add(raw_materials_frame, text="Raw Materials",padding=10)

bottle_inventory_notebook.add(production_frame, text="Production Log",padding=10)
production_frame.bind('<Visibility>',lambda event: view_products('production','null','All',production_table))

bottle_inventory_notebook.add(inprog_fr,text="In Progress",padding=10)


bottle_inventory_notebook.add(bottle_frame, text="Bottle Inventory",padding=10)
bottle_frame.bind('<Visibility>',lambda event: view_products('bottles','null','All',bottle_table))

bottle_inventory_notebook.add(samples_frame,text="Samples",padding=10)


bottle_inventory_notebook.pack(side=BOTTOM,fill=BOTH,expand=1)

raw_materials_table = Treeview_Table(raw_materials_frame,("Type","Product","Amount","Price","Total"))

#show table upon opening application
view_products('raw_materials','null','All',raw_materials_table)

#create raw materials command frame and populate with view and options buttons
raw_materials_command_frame = Command_Frame(raw_materials_frame)

raw_materials_view_frame = View_Frame(raw_materials_command_frame,'raw_materials',raw_materials_table,["Bottles","Boxes","Caps","Capsules","Labels","All"])

raw_materials_option_frame = Option_Frame(raw_materials_command_frame)
Logistics_Button(raw_materials_option_frame,"Add Item",'raw_materials',raw_materials_table,lambda: Add_View(window,'raw_materials',raw_materials_table,1))
Logistics_Button(raw_materials_option_frame,"Production",'raw_materials',raw_materials_table,lambda: Production_View(window,'bottles',raw_materials_table))
Logistics_Button(raw_materials_option_frame,"Edit Selection",'raw_materials',raw_materials_table,lambda: edit_check('raw_materials',raw_materials_table,raw_edit))

Total_Label("raw_materials",raw_materials_command_frame)

raw_materials_option_frame.pack()
raw_materials_command_frame.pack(padx=10)

production_table = Treeview_Table(production_frame,("Date","Product","Amount"))

#create production commands frame and populate with an edit button
production_command_frame = Command_Frame(production_frame)

production_opt_frame = Option_Frame(production_command_frame)
Logistics_Button(production_opt_frame,"Edit Selection",'production',production_table,lambda: edit_check('production',production_table,production_edit))

production_opt_frame.pack()
production_command_frame.pack(padx=10)

inprog_tbl = Treeview_Table(inprog_fr,("Date","Product","Amount","Case Size"))

inprog_cfr = Command_Frame(inprog_fr)

inprog_optfr = Option_Frame(inprog_cfr)
Logistics_Button(inprog_optfr,"Edit Selection",'in_progress',inprog_tbl,lambda: edit_check('in_progress',inprog_tbl,in_progress_edit))

inprog_optfr.pack(padx=10)
inprog_cfr.pack(padx=10)

bottle_table = Treeview_Table(bottle_frame,("Type","Product","Amount","Price","Total"))

#create bottle command frame and populate with view and option buttons
bottle_command_frame = Command_Frame(bottle_frame)

bottle_view_frame = View_Frame(bottle_command_frame,'bottles',bottle_table,["Vodka","Whiskey","Rum","Other","All"])

bottle_option_frame = Option_Frame(bottle_command_frame)
Logistics_Button(bottle_option_frame,"Add Item",'bottles',bottle_table,lambda: Add_View(window,'bottles',bottle_table,1))
Logistics_Button(bottle_option_frame,"Edit Selection",'bottles',bottle_table,lambda: edit_check('bottles',bottle_table,bottles_edit))

Total_Label("bottles",bottle_command_frame)

bottle_option_frame.pack()
bottle_command_frame.pack(padx=10)

#create grain inventory notebook, populate with tabbed frames
grain_inventory_notebook = ttk.Notebook(window, height=height, width=width)
grain_inventory_frame = ttk.Frame(grain_inventory_notebook)
grain_inventory_notebook.add(grain_inventory_frame, text="Grain Inventory", padding=10)

#create grain inventory table and pack within grain frame
grain_table = Treeview_Table(grain_inventory_frame,("Order No","Type","Amount","Price","Total"))

#create grain command frame and populate with option buttons
grain_command_frame = Command_Frame(grain_inventory_frame)

grain_option_frame = Option_Frame(grain_command_frame)
Logistics_Button(grain_option_frame,"Produce Mash",'grain',grain_table,None)
Logistics_Button(grain_option_frame,"Mash Production Sheet",'grain',grain_table,None)
Logistics_Button(grain_option_frame,"Add Grain",'grain',grain_table,lambda: Add_View(window,'grain',grain_table,1))
Logistics_Button(grain_option_frame,"Edit Selection",'grain',grain_table, lambda: edit_check('grain',grain_table,grain_edit))

Total_Label('grain',grain_command_frame)

grain_option_frame.pack()
grain_command_frame.pack(padx=10)

#create barrel inventory notebook and populates with tabbed frames
barrel_inventory_notebook = ttk.Notebook(window, height=height, width=width)
barrel_frame = ttk.Frame(barrel_inventory_notebook)
barrel_inventory_notebook.add(barrel_frame, text="Barrel Inventory",padding=10)

#create barrel inventory table
barrel_table = Treeview_Table(barrel_frame,("Barrel No","Type","Proof Gallons","Date Filled","Age","Investor"))

#create barrel command frame and populate with view and option buttons
barrel_command_frame = Command_Frame(barrel_frame)

barrel_view_frame = View_Frame(barrel_command_frame,'barrels',barrel_table,["Bourbon","Rye","Malt","Other","All"])

barrel_option_frame = Option_Frame(barrel_command_frame)
Logistics_Button(barrel_option_frame,"Add Barrel",'barrels',barrel_table,lambda: Add_View(window,'barrels',barrel_table,1))
Logistics_Button(barrel_option_frame,"Edit Selection",'barrels',barrel_table, lambda: edit_check('barrels',barrel_table,barrel_edit))

barrel_option_frame.pack()
barrel_command_frame.pack(padx=10)

#create purchase orders notebook with tabbed frames
purchase_orders_notebook = ttk.Notebook(window,height=height,width=width)
purchase_orders_frame = Frame(purchase_orders_notebook)
purchase_orders_notebook.add(purchase_orders_frame,text="Purchase Orders",padding=10)

#create purchase orders table
purchase_orders_table = Treeview_Table(purchase_orders_frame,("Date","Product","Amount","Price","Total","Destination","PO No."))

#create purchase orders command frame and populate with option buttons
purchase_orders_command_frame = Command_Frame(purchase_orders_frame)

purchase_orders_option_frame = Option_Frame(purchase_orders_command_frame)
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
employee_transactions_command_frame = Command_Frame(employee_transactions_frame)

employee_transactions_options_frame = Option_Frame(employee_transactions_command_frame)
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
