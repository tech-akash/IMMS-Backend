import logging
from .models import RegisteredStudent
from datetime import date
from django.contrib.auth.models import User
from .models import *
from datetime import datetime,timedelta
import pytz
from .helpers import GetDayTime
ist = pytz.timezone('Asia/Kolkata')

def my_cron_job():
    x=datetime.now(ist).date()
    allUser=User.objects.all()
    day,time=GetDayTime()
    for user in allUser:
        check=checkAlreadyEaten.objects.filter(user=user)
        if check:
            continue
        leave=Leave.objects.filter(user=user,start_date__lte=x,end_date__gte=x)
        noteating=NotEatingToday.objects.filter(user=user,date = x,time=time)
        if (not leave) and (not noteating):
            silverToken=SilverToken.objects.filter(user=user,tokenDate=x,tokenTime=time)
            if not silverToken:
                goldToken=GoldToken.objects.get(user=user)
                if goldToken.TokenCount>0:
                    goldToken.TokenCount-=1
                    goldToken.save()
            else:
                silverToken.delete()
    y=checkAlreadyEaten.objects.all().count()
    checkAlreadyEaten.objects.all().delete()


def get_registered_user():
    tomorrow=(datetime.now(ist)+timedelta(1)).date()
    # tommorow=x
    today=datetime.now(ist).date()
    allUser=User.objects.all()
    day,time=GetDayTime()
    breakfast=0
    lunch=0
    dinner=0

    for user in allUser:
        leave=Leave.objects.filter(user=user,start_date__lte=tomorrow,end_date__gte=tomorrow)
        noteating=NotEatingToday.objects.filter(user=user,date = tomorrow)
        if not leave :
            # pass
            silverToken=SilverToken.objects.filter(user=user,tokenDate__lte=tomorrow,tokenDate__gte=today).count()
            goldToken=GoldToken.objects.get(user=user)
            goldTokenCount = goldToken.TokenCount
            if silverToken+goldTokenCount>=6:
                breakfast+=1
                lunch+=1
                dinner+=1
                for y in noteating:
                    if y.time==0:
                        breakfast-=1
                    elif y.time==1:
                        lunch-=1
                    else:
                        dinner-=1

            elif silverToken+goldTokenCount==5:
                breakfast+=1
                lunch+=1
                z=1
                cnt=len(noteating)
                for y in noteating:
                    if y.time==0:
                        breakfast-=1
                    elif y.time==1:
                        lunch-=1
                    else:
                        z=0
                if cnt>0:
                    dinner+=z
            elif silverToken+goldTokenCount==4:
                breakfast+=1
                z=1
                y=1
                cnt=len(noteating)
                for y in noteating:
                    if y.time==0:
                        breakfast-=1
                    elif y.time==1:
                        y=0
                    else:
                        z=0
                if cnt>0:
                    lunch+=y
                    if y==1:
                        cnt-=1
                
                if cnt>0:
                    dinner+=z

    RegisteredStudent.objects.create(date=tomorrow,breakfast=breakfast,lunch=lunch,dinner=dinner)


    

    