import sqlite3

def database():
    global conn,cur
    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS bottles (id INTEGER PRIMARY KEY,item TEXT, amount INTEGER)")
    #cur.execute("INSERT INTO bottles VALUES (NULL,?,?)", ('',120))
    conn.commit()

def view_widget(window,widget,padx,location):

    for widg in window.pack_slaves():
        widg.pack_forget()

    widget.pack(padx=padx, side=location)
