import sqlite3

class Database:

    def __init__(self):
        self.conn = sqlite3.Connection("balance.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS balance (date TEXT, amount REAL)")
        self.conn.commit()


    def change_balance(self,date, amount):
        self.cur.execute("INSERT INTO balance VALUES (?,?)", (date,amount))
        self.conn.commit()

    def view(self):
        global rows
        self.cur.execute("SELECT * FROM balance")
        self.rows = self.cur.fetchall()

    def __del__(self):
        self.conn.close()
