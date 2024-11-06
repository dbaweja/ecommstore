from django.shortcuts import render
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

class PaymentView(APIView):
    def __init__(self):
        super().__init__()

    def post(self, request):
        pass
# Create your views here.
