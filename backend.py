import sqlite3

class Balance_Database:

    def __init__(self, database):
        self.conn = sqlite3.Connection(database)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS balance (date TEXT, amount REAL)")
        self.conn.commit()

        #update balance database
    def change_balance(self,date,amount):
        self.cur.execute("INSERT INTO balance VALUES (?,?)", (date,amount))
        self.conn.commit()

        #view balance database
    def view(self):
        global rows
        self.cur.execute("SELECT * FROM balance")
        self.rows = self.cur.fetchall()

    def __del__(self):
        self.conn.close()

class Transaction_Database:

    def __init__(self, database):
        self.conn = sqlite3.Connection(database)
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS transactions (date TEXT, amount REAL, location TEXT, type TEXT)")
        self.conn.commit()

        #change transaction database
    def change_balance(self,date,amount,location,type):
        self.cur.execute("INSERT INTO transactions VALUES (?,?,?,?)", (date,amount,location,type))
        self.conn.commit()

        #view transaction database
    def view(self):
        global rows
        self.cur.execute("SELECT * FROM transactions")
        self.rows = self.cur.fetchall()
        print(self.rows)


    def __del__(self):
        self.conn.close()
