import sqlite3

class Bottle_Database:

    def __init__(self, database):
        self.conn = sqlite3.Connection(database)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS bottles (id INTEGER PRIMARY KEY,item TEXT, amount REAL)")
        self.conn.commit()

        #update bottles database
    def insert(self,item,amount):
        self.cur.execute("INSERT INTO bottles VALUES (NULL,?,?)", (item,amount))
        self.conn.commit()

        #view bottles database
    def view(self):
        global rows
        self.cur.execute("SELECT * FROM bottles")
        self.rows = self.cur.fetchall()

    def __del__(self):
        self.conn.close()

class Raw_Materials_Database:

    def __init__(self,database):
        self.conn = sqlite3.Connection(database)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS 'raw materials' (id INTEGER PRIMARY KEY,item TEXT, amount REAL)")
        self.conn.commit()

    #update raw materials database
def insert(self,item,amount):
    self.cur.execute("INSERT INTO 'raw materials' VALUES (NULL,?,?)", (item,amount))
    self.conn.commit()

    #view raw materials database
def view(self):
    global rows
    self.cur.execute("SELECT * FROM 'raw materials'")
    self.rows = self.cur.fetchall()

def __del__(self):
    self.conn.close()
