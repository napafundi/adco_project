import products

ALB_1L = products.Bottle("1L",6,20.00,"ALB 1L","20mm","White","ALB Box")

for i in ALB_1L.__dict__.items():

    print(i[1])

import inventory
