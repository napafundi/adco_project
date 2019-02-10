from tkinter import *
from tkinter import ttk

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
