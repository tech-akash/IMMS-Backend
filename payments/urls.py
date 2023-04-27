from django.urls import path
from .views import StripeCheckoutView,get_status


urlpatterns = [
    path('create-checkout-session',StripeCheckoutView.as_view()),
    path('check-status/<str:session_id>',get_status),
]
