

from django.contrib.auth.decorators import login_required
# from django.shortcuts import render
from django.shortcuts import render
from allauth.socialaccount.providers.google.views import GoogleOAuth2Adapter
from dj_rest_auth.registration.views import SocialLoginView
from allauth.socialaccount.providers.oauth2.client import OAuth2Client
from rest_framework_simplejwt.views import TokenRefreshView
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.http import Http404
from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from .serializers import *
from .models import *
from django.db.models.functions import Now
from django.utils import timezone
from .helpers import GetDayTime
from django.contrib.auth.models import User
from datetime import date
from django.utils import timezone
from datetime import datetime,timedelta
import pytz
from django.views.decorators.csrf import csrf_exempt

ist = pytz.timezone('Asia/Kolkata')
# class GoogleLogin(SocialLoginView):
#     authentication_classes = [] # disable authentication
#     adapter_class = GoogleOAuth2Adapter
#     callback_url = "http://localhost:3000/login"
#     client_class = OAuth2Client
    

# @csrf_exempt
# def google_token(request):
#     print (request.POST)
#     if "code" in request.POST:
#         # print("hii")
#         from rest_framework_simplejwt.settings import api_settings as jwt_settings
#         from rest_framework_simplejwt.views import TokenRefreshView
        
#         class RefreshNuxtAuth(TokenRefreshView):
#             # By default, Nuxt auth accept and expect postfix "_token"
#             # while simple_jwt library doesnt accept nor expect that postfix
#             def post(self, request, *args, **kwargs):
#                 request.data._mutable = True
#                 request.data["refresh"] = request.data.get("refresh_token")
#                 request.data._mutable = False
#                 response = super().post(request, *args, **kwargs)
#                 response.data['refresh_token'] = response.data['refresh']
#                 response.data['access_token'] = response.data['access']
#                 return response

#         return RefreshNuxtAuth.as_view()(request)
#     else:
#         return GoogleLogin.as_view()(request)


@api_view(['POST'])
def login_view(request):
    print(request.data)
    data=request.data
    print(data['token']['email'])
    username=data['token']['sub']
    email=data['token']['email']
    firstName=data['token']['given_name']
    lastName=data['token']['family_name']
    type=None
    try:
        # print('user logged in')
        user=User.objects.get(username=username)
        type=Student.objects.get(user=user).type

    except:
        # print('user created')
        User.objects.create(username=username,password=email)
        user=User.objects.get(username=username)
        type='Student'
        Student.objects.create(user=user,FirstName=data['token']['given_name'],LastName=data['token']['family_name'],email=email,type='Student')
        GoldToken.objects.create(user=user)
    return Response({'status':200,'type':type,'username':username,'firstname':firstName,'lastname':lastName,'email':email})



@login_required
def test_view(request):
    return render(request, 'test.html')


@api_view(['GET'])
def get_menu(request,*args, **kwargs):
    obj=Menu.objects.all()
    serializer=MenuSerializer(obj,many=True)
    return Response(serializer.data)

@api_view(['GET'])
def home_view(request,*args,**kwargs):
    obj=Menu.objects.all()
    serializer=MenuSerializer(obj,many=True)
    return Response(serializer.data)

# @csrf_exempt
@api_view(['POST'])
def update_menu(request,*args, **kwargs):
    print(request.data)
    try: 
        obj=Menu.objects.get(day=request.data['day'],time=request.data['time'])
        if request.method == 'POST':
            # print(request.POST)
            print("data:", request.data)
            serializer=MenuSerializer(obj,data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            else:
                return Response(serializer.errors)
        else:
            serializer=MenuSerializer(obj)
            return Response(serializer.data)
    except:
        return Response({'status':400,'message':'something went wrong'})

# @csrf_exempt
@api_view(['POST'])
def giveFeedback(request,*args, **kwargs):
    # print(request.POST)
    # print(request.data['_content']['username'])
    try:
        user=User.objects.get(username=request.data['username'])
        serializer=FeedbackSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors)
    except:
        return Response({'status':400,'message':'something went wrong'})


@api_view(['GET'])
def getFeedback(request,*args, **kwargs):
    obj=Feedback.objects.all()
    serializer=ViewFeedbackSerializer(obj,many=True)
    return Response(serializer.data)
    


@api_view(['GET','POST'])
def viewSilverToken(request,*args, **kwargs):
    if request.method=='POST':
        try:
            day=request.data['day']
            time=request.data['time']
            obj=Menu.objects.get(day=day,time=time)
            
            return Response({'order_value':obj.price})
        except:
            return Response({'status':400,'message':'something went wrong'})
    else:
        return Response({'status':200})


# @api_view(['GET','POST'])
# def viewSilverToken(request,*args, **kwargs):
#     if request.method=='POST':
#         day=request.data['day']
#         time=request.data['time']
#         obj=Menu.objects.get(day=day,time=time)
        
#         return Response({'order_value':obj.price})
#     else:
#         return Response({'status':200})
    



@api_view(['GET','POST'])
def viewGoldToken(request,*args, **kwargs):
    if request.method=='POST':
        tokenCount=request.data['count']
        obj=GoldTokenPrice.objects.get(TokenCount=tokenCount)
        
        return Response({'token_count':obj.TokenCount,'order_value':obj.Price})
    else:
        return Response({'status':200}) 





@api_view(['POST'])
def ShowTokens(request,*args, **kwargs):
    user=User.objects.get(username=request.data['username'])
    x=datetime.now(ist).date()
    obj=SilverToken.objects.filter(user=user,tokenDate__gte=x)
    obj1=GoldToken.objects.get(user=user)
    # print(obj,obj1)
    tokens={}
    tokens['silver']=SilverTokenSerializers(obj,many=True).data
    tokens['gold']=obj1.TokenCount
    return Response(tokens)

# @api_view(['GET'])
# def HaveToken(request,*args, **kwargs):
#     day,time=GetDayTime()
#     obj=NotEatingToday.objects.filter(user=request.user,day=day,time=time)
#     print(obj)
#     if obj:
#         return Response({"flag":False})
#     else:
#         obj1=SilverToken.objects.filter(user=request.user,expiryTime__lt=Now(),time=time,day=day)
#         obj2=GoldToken.objects.get(user=request.user)
#         if obj1:
#             return Response({"flag":True})
#         elif obj2.TokenCount>0:
#             return Response({"flag":True})
#         else:
#             return Response({"flag":False})


# @api_view(['GET'])
# def EatenToday(request,*args, **kwargs):
#     day,time=GetDayTime()
    
    

    
@api_view(['GET'])
def NumberofPeople(request,*args, **kwargs):
    today=datetime.now(ist).date()
    tomorrow=(datetime.now(ist)+timedelta(1)).date()
    obj=RegisteredStudent.objects.filter(date=today).last()
    allUser=User.objects.all()
    if not obj:
        breakfast=0
        lunch =0
        dinner=0
        day,time=GetDayTime()
        for user in allUser:
            leave=Leave.objects.filter(user=user,start_date__lte=today,end_date__gte=today)
            noteating=NotEatingToday.objects.filter(user=user,date = today)
            if not leave :
            # pass
                silverToken=SilverToken.objects.filter(user=user,tokenDate__lte=tomorrow,tokenDate__gte=today).count()
                goldToken=GoldToken.objects.get(user=user)
                goldTokenCount = goldToken.TokenCount
                if silverToken+goldTokenCount>=3:
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

                elif silverToken+goldTokenCount==2:
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
                elif silverToken+goldTokenCount==1:
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
        RegisteredStudent.objects.create(date=today,breakfast=breakfast,lunch=lunch,dinner=dinner)
    obj=RegisteredStudent.objects.filter(date=today).last()
    tom_breakfast=0
    tom_lunch=0
    tom_dinner=0
    for user in allUser:
        leave=Leave.objects.filter(user=user,start_date__lte=tomorrow,end_date__gte=tomorrow)
        noteating=NotEatingToday.objects.filter(user=user,date = tomorrow)
        if not leave :
            # pass
            silverToken=SilverToken.objects.filter(user=user,tokenDate__lte=tomorrow,tokenDate__gte=today).count()
            goldToken=GoldToken.objects.get(user=user)
            goldTokenCount = goldToken.TokenCount
            if silverToken+goldTokenCount>=6:
                tom_breakfast+=1
                tom_lunch+=1
                tom_dinner+=1
                for y in noteating:
                    if y.time==0:
                        tom_breakfast-=1
                    elif y.time==1:
                        tom_lunch-=1
                    else:
                        tom_dinner-=1

            elif silverToken+goldTokenCount==5:
                tom_breakfast+=1
                lunch+=1
                z=1
                cnt=len(noteating)
                for y in noteating:
                    if y.time==0:
                        tom_breakfast-=1
                    elif y.time==1:
                        tom_lunch-=1
                    else:
                        z=0
                if cnt>0:
                    tom_dinner+=z
            elif silverToken+goldTokenCount==4:
                tom_breakfast+=1
                z=1
                y=1
                cnt=len(noteating)
                for y in noteating:
                    if y.time==0:
                        tom_breakfast-=1
                    elif y.time==1:
                        y=0
                    else:
                        z=0
                if cnt>0:
                    tom_lunch+=y
                    if y==1:
                        cnt-=1
                
                if cnt>0:
                    tom_dinner+=z
    # obj1=RegisteredStudent.objects.filter(date=tomorrow).last()
    return Response({'today':{
        '0':obj.breakfast,
        '1':obj.lunch,
        '2':obj.dinner
    },
    'tommorow':{
        '0':tom_breakfast,
        '1':tom_lunch,
        '2':tom_dinner
    }})
    # users=User.objects.all()
    # day,time=GetDayTime()
    # if request.method=='POST':
    #     day=request.data['day']
    #     time=request.data['time']
    # cnt=0
    # for user in users:
    #     try:
    #         obj=SilverToken.objects.get(user=user,tokenDate=date.today(),tokenTime=time)
    #         obj1=GoldToken.objects.get(user=user)
    #         if obj:
    #             cnt+=1
    #         elif obj1.TokenCount>0:
    #             cnt+=1
    #     except:
    #         pass
    
    # return Response({"StudentCount":cnt})





# @api_view(['GET','POST'])
# def checkSilverToken(request,*args, **kwargs):
#     obj = SilverToken.objects.filter(user=request.user)
#     if request.method == 'POST':
#         data = request.data
#         serializer=CheckSilverTokenSerializer(obj,data=data)
#         if serializer.is_valid():
#                 curr_date = timezone.now().date()
#                 tokenObj = SilverToken.objects.filter(user=data['user'], time=data['time'], day=data['day'])
#                 if tokenObj:
#                     if  tokenObj[0].expiryDate == curr_date:
#                         return Response({'status':'success'})
#                     else:
#                         print()
#                         return Response({'status':'failed'})
                    
#                 else:
#                     return Response({'status':'failed'})
#         else:  
#             return Response({'status':'failed'})
                      
#     else:
#         serializer=CheckSilverTokenSerializer(obj, many=True)
#         return Response(serializer.data)


# @api_view(['GET','POST'])
# def checkGoldToken(request,*args, **kwargs):
#     obj = GoldToken.objects.filter(user=request.user)
#     if request.method == 'POST':
#         data = request.data
#         serializer=CheckGoldTokenSerializer(obj,data=data, partial=True)
#         if serializer.is_valid():
#                 try: 
#                     tokenObj = GoldToken.objects.filter(user=data['user'], time=data['time'])
#                     if tokenObj:
#                         curr_date =timezone.now().date()
#                         if tokenObj[0].TokenCount>0 and tokenObj[0].TokenExpiry<=curr_date:
#                             tokenObj[0].TokenCount-=1
#                             tokenObj[0].save()
#                             return Response({'status':'success'})
#                     else:
#                         return Response({'status':'failed'})
#                 except:
#                         return Response({'status':'failed'})
                    
#         else:  
#             return Response({'status':'failed'})
                      
#     else:
#         serializer=CheckGoldTokenSerializer(obj, many=True)
#         return Response(serializer.data)


@api_view(['POST'])

def scanQr(request,*args, **kwargs):
    user=User.objects.get(username=request.data['username'])
    day,time=GetDayTime()
    x=datetime.now(ist).date()
    y=checkAlreadyEaten.objects.filter(user=user,date=x,time=time)
    try:
        obj=TakenMeal.objects.get(date=y)
    except:
        obj=TakenMeal.objects.create(date=y)
    
    if y:
        return Response({'status':401,'message':'You have already eaten'})
    leave=Leave.objects.filter(user=user,start_date__lte=x,end_date__gte=x)
    if not leave:
        noteating=NotEatingToday.objects.filter(user=user,date = x,time=time)
        if not noteating:
            silverToken=SilverToken.objects.filter(user=user,tokenDate=x,tokenTime=time)
            if not silverToken:
                goldToken=GoldToken.objects.get(user=user)
                if goldToken.TokenCount>0:
                    goldToken.TokenCount-=1
                    goldToken.save()
                    checkAlreadyEaten.objects.create(user=user,date=x,time=time)
                    if time ==0:
                        obj.breakfast+=1
                    elif time==1:
                        obj.lunch+=1
                    else:
                        obj.dinner+=1
                    obj.save()
                    return Response({'status':200,'message':'Gold Token is Used'})
                return Response({'status':400,'message':'You don\'t have any token'})
            else:
                silverToken.delete()
                if time ==0:
                    obj.breakfast+=1
                elif time==1:
                    obj.lunch+=1
                else:
                    obj.dinner+=1
                checkAlreadyEaten.objects.create(user=user,date=x,time=time)
                obj.save()
                return Response({'status':200,'message':'Silver Token is Used'})
        else:
            return Response({'status':401,'message':'You filled for the leave'})
    else:
        return Response({'status':401,'message':'You filled for the leave'})
    
@api_view(['POST'])
def cancelMeal(request,*args, **kwargs):
    try:
        user=User.objects.get(username=request.data['username'])
        # day,time=GetDayTime()
        date=request.data['date']
        time=request.data['time']
        NotEatingToday.objects.create(user=user,date=date,time=time)
        return Response({'status':200})
    except:
        return Response({'status':400})


@api_view(['POST'])
def leaveView(request,*args, **kwargs):
    try:
        user=User.objects.get(username=request.data['username'])
        start_date=request.data['startDate']
        end_date=request.data['endDate']
        Leave.objects.create(user=user,start_date=start_date,end_date=end_date)
        return Response({'status':200})
    except:
        return Response({'status':400})
    

@api_view(['GET'])
def getReport(request,*args, **kwargs):
    list=[]
    for x in range(1,2):
        date=(datetime.now(ist)-timedelta(x)).date()
        print(date)
        register_student=0
        # print(obj1.dinner)

        try:
            # print('hiii')
            obj1=TakenMeal.objects.filter(date=date).last()
            obj=RegisteredStudent.objects.filter(date=date).last()
            # print(obj)
            list.append({'date':date,'registeredBreakfast':obj.breakfast,'registeredLunch':obj.lunch,'registeredDinner':obj.dinner,'takenMealBreakfast':obj1.breakfast,'takenMealLunch':obj1.lunch,'takenMealDinner':obj1.dinner})
        except:
            print("error")
            pass

        
    return Response(list)



