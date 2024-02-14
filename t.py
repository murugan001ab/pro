import datetime
import time

x=datetime.datetime.now()
y=x.strftime("%I:%M:%S %P")
z=x.strftime("%m:%M")
print(x.strftime("%d/%m/%Y"))
print(y)
x=time.time()
print(x)

id="hacker.db"
i=id.split(".")
print(i[0])