from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .service import PaymentService
from store.serializers import OrderSerializer
from store.models import Order
from pprint import pprint
import uuid
class PaymentView(APIView):
    def __init__(self):
        super().__init__()
        self.service = PaymentService()

    def post(self, request):
        pprint("Received a POST request at Payment")
        order_data = request.data
        order_data['order_id'] = str(uuid.uuid4())
        order_serialized = OrderSerializer(data=request.data)
   #     pprint(order_serialized.data)
        pprint("Order has been serialized")
        if order_serialized.is_valid():
            try:
                pprint(order_serialized)
                order = order_serialized.save()
                pprint(f"Order is validated. Order details: {order}")
                try:
                    pprint("Getting payment link")
                    payment_link = self.service.initiate_payment(order.order_id, order.amount)
                    pprint("Got payment link")
                    return Response({"payment_link": payment_link}, status=status.HTTP_200_OK)
                except Exception as e:
                    pprint("An exception was encountered")
                    return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            except Exception as e:
                pprint(f"Error while saving the order: {e}")
                return Response({"error": "Failed to create the order."}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # If serializer validation fails, return errors
            pprint(f"Order validation failed. Errors: {order_serialized.errors}")
            return Response(order_serialized.errors, status=status.HTTP_400_BAD_REQUEST)