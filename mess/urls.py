from django.urls import path
from .views import *
urlpatterns = [

    path('auth/',login_view,name='login'),
    path('',home_view,name="home"),
    path('update-menu/',update_menu),
    path('give-feedback/',giveFeedback),
    path('buy-single-token/',viewSilverToken,name='token'),    
    path('view-feedback/',getFeedback),
    path('get-registered/',NumberofPeople),
    # path('check-silver-token/', checkSilverToken),
    # path('check-gold-token/', checkGoldToken),
    path('auth/login/',login_view),
    path('scan/',scanQr),
    path('get-tokens/',ShowTokens),
    path('test/', test_view, name='test_view'),
    path('menu/',get_menu),
    path('cancel-meal/',cancelMeal),
    path('leave/',leaveView),
    path('get-report/',getReport),
    path('get-all-transactions/',getallUserTransactions),
    path('get-my-transactions/',getuserTransactions),

]
