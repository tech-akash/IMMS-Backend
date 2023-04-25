from datetime import datetime
import pytz
ist = pytz.timezone('Asia/Kolkata')
def GetDayTime():
    x=datetime.now(ist)
    day=x.weekday()
    time1=x.hour
    time=0
    if time1<12:
        time=0
    elif time<14:
        time=1
    else:
        time=2
    return day,time
