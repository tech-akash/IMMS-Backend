

from django.conf import settings
from rest_framework.views import APIView
import stripe
# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from django.contrib.auth.models import User
from mess.models import *

class StripeCheckoutView(APIView):
    def post(self,request):

        try:
            price=['price_1MzcRsSGJ3YbEH6gsHdAUEZy','price_1MzcSoSGJ3YbEH6gvSFfWpz4','price_1MzcTLSGJ3YbEH6gvliTHP3m']
            x=int(request.data['id'])
            print (x)

            print(type(x))
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        'price': price[x],
                        'quantity': 1,
                    },
                ],
                mode='payment',
                success_url=settings.SITE_URL + '/?success=true&session_id={CHECKOUT_SESSION_ID}',
                cancel_url=settings.SITE_URL + '?canceled=true',
            )
            return redirect(checkout_session.url)
        except:
            return Response({
                'error':'Something went wrong when creating stripe checkout session'},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

@api_view(['POST'])
def get_status(request,session_id):
        # session_id = request.GET.get('session_id')
        print(session_id)
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            print(session)
            payment_status = session.payment_status
            if payment_status == 'paid':
                username=request.data['username']
                user=User.objects.get(username=username)
                token=request.data['token']
                if token=='0':
                    date=request.data['date']
                    time=request.data['time']

                    SilverToken.objects.create(user=user,tokenDate=date,tokenTime=time)
                else:
                    goldToken=GoldToken.objects.get(user=user)
                    if token=='1':
                        goldToken.TokenCount+=45
                        goldToken.save()
                    else:
                        goldToken.TokenCount+=90
                        goldToken.save()
                     
                 
            return Response({'status': payment_status})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


