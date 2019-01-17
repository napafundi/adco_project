from datetime import datetime
import math

date1 = "01-01-2000"
date2 = "02-01-2010"

date1 = datetime.strptime(date1,"%m-%d-%Y")
date2 = datetime.strptime(date2,"%m-%d-%Y")
print(date1)
print(date2)
print("Time passed is %d years, %d months" % (math.floor((date2 - date1).days/365.2425),((date2 - date1).days%365.2425)/30))
