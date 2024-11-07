from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .service import PaymentService
from store.serializers import OrderSerializer
from store.models import Order

class PaymentView(APIView):
    def __init__(self):
        super().__init__()
        self.service = PaymentService()

    def post(self, request):
        order_serialized = OrderSerializer(data=request.data)
        if order_serialized.is_valid():
            order = order_serialized.save()
            try:
                payment_link = self.service.initiate_payment(order.order_id, order.amount)
                return Response({"payment_link": payment_link}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
