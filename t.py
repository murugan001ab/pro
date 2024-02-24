import datetime
import time

x=datetime.datetime.now()
y=x.strftime("%I:%M:%S %P")
z=x.strftime("%m:%M")
print(x.strftime("%Y"))
print(y)
x=time.time()
print(x)

id="hacker.db"
i=id.split(".")
print(i[0])

name="naresh.db"
cname=str(name).split('.')[0]
print(cname)
