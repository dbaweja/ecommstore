from django.urls import path
from payment.views import PaymentView

urlpatterns = [
    path('', PaymentView.as_view(), name='payment'),
]