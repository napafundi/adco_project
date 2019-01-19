from tkinter import *
from tkinter import ttk

class Treeview_Table(ttk.Treeview):
    def __init__(self,master,columns):
        ttk.Treeview.__init__(self,master,columns=columns,show='headings',height=600,style="Custom.Treeview")
        self.width=int(796/(len(columns)))
        self.columns = columns
        for i in range(len(columns)):
            self.column(self.columns[i],anchor='center',width=self.width)
            self.heading(str('#' + str((i+1))),text=self.columns[i])
        self.pack(side=RIGHT,fill=Y)


window = Tk()

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
raw_materials_table = Treeview_Table(raw_materials_frame,("Type","Item","Amount","Price","Total"))



mainloop()
