

from django.conf import settings
from rest_framework.views import APIView
import stripe
# This is your test secret API key.
stripe.api_key = settings.STRIPE_SECRET_KEY
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import redirect


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
    def get(self, request):
        session_id = request.GET.get('session_id')
        try:
            session = stripe.checkout.Session.retrieve(session_id)
            payment_status = session.payment_status
            return Response({'status': payment_status})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


