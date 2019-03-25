import sqlite3


conn = sqlite3.Connection("inventory.db")
cur = conn.cursor()
cur.execute("SELECT mash_no, type " +
                   "FROM mashes " +
               "ORDER BY date " +
             "DESC LIMIT 1")
prev_mash = list(cur)[0]
prev_mash_num = prev_mash[0]
prev_mash_type = prev_mash[1]
conn.close()
#Mash number regex matches.
mo = mashRegex.search(prev_mash_num)
year = mo.group(1)    #Prev mash's year.
mash_count = mo.group(5)  #Prev mash's ID number.
mash_letter = mo.group(6) #Prev mash's letter variable.
mash_letters = list(string.ascii_uppercase[:8]) #Letters A-H
