import sqlite3

def database():
    global conn,cur
    conn = sqlite3.Connection("inventory.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS bottles (id INTEGER PRIMARY KEY,item TEXT, amount INTEGER)")
    #cur.execute("INSERT INTO bottles VALUES (NULL,?,?)", ('',120))
    conn.commit()
