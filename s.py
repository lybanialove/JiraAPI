from datetime import datetime,timedelta
from dateutil import parser

d = datetime.now()
nd = timedelta(days=d.day,seconds=d.second,hours=d.hour,minutes=d.minute)
p = parser.parse("2024-07-08T16:39:14.532907")
pd = timedelta(days=p.day,seconds=p.second,hours=p.hour,minutes=p.minute)

print(nd - pd)