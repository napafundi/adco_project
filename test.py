import sqlite3


conn = sqlite3.Connection("inventory.db")
cur = conn.cursor()
cur.execute("SELECT * FROM in_progress")
columns = [x[0] for x in cur.description]
print(columns)
str1 = "=?, ".join(columns) + "=?"
str2 = "=? AND ".join(columns) + "=?"
sqlite = "in_progress"

print("UPDATE " + sqlite + " SET " + str1 + " WHERE " + str2 )
