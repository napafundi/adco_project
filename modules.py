import sqlite3

def database():
    global conn,cur
    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS bottles (id INTEGER PRIMARY KEY,item TEXT, amount REAL)")
    conn.commit()


def display_database() :
    cur.execute("SELECT * FROM bottles")
    rows = cur.fetchall()
    for row in rows:
        tree.insert("",END,values = row)
