from tkinter import *
from tkcalendar import Calendar

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
def example1():
    def print_sel():
        print(cal.selection_get())

    top = Toplevel(window)

    cal = Calendar(top, font="Arial 14", selectmode='day', locale='en_US',
                   cursor="hand2", year=2018, month=2, day=5)

    cal.pack(fill="both", expand=True)
    Button(top, text="ok", command=print_sel).pack()

Button(window, text='Calendar', command=example1).pack(padx=10, pady=10)
window.mainloop()
