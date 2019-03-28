from tkinter import *
from datetime import datetime
from tkinter import ttk

class Reports_Frame(Frame):
    #Creates frame containing inventory information from each sqlite
    #table.
    def __init__(self, master):
        self.master = master
        self.cur_year = datetime.now().year
        Frame.__init__(self, master)

        self.year_cmbo_box = ttk.Combobox(
            self, values=list(range(2019, self.cur_year + 1)))
        self.year_cmbo_box.grid(row=0, column=0)
window = Tk()
frame = Reports_Frame(window)
print(type(Reports_Frame))
