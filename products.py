import sqlite3

class Bottle:

    def __init__(self,size,case_size,price,label,cap,capsule,box):
        self.size = size
        self.case_size = case_size
        self.price = price
        self.label = label
        self.cap = cap
        self.capsule = capsule
        self.box = box

    def produce(self, production_amount, id):
        self.conn = sqlite3.Connection("bottle_inventory.db")
        self.cur = self.conn.cursor()
        self.cur.execute("Update bottles SET amount = amount - production_amount WHERE ID = id")
        self.conn.commit()
