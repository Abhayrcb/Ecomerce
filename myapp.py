import datetime



yt = int(datetime.date.today().strftime('%Y'))
print(yt)
mt = int(datetime.date.today().strftime('%m'))
print(mt)
dt = int(datetime.date.today().strftime('%d'))
print(dt)
d = (datetime.date(yt,mt,dt))
print(d)
current_date =d.strftime('%y%m%d')
print(datetime.date(yt,mt,dt))
print(d)