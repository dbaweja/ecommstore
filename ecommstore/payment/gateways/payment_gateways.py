from abc import ABC, abstractmethod
import razorpay
import json
from ecommstore import settings

class PaymentGateway(ABC):
    @abstractmethod
    def generate_payment_link(self, order_id, amount):
        pass

class RazorpayPaymentGateway(PaymentGateway):
    def __init__(self):
        self.client = razorpay.Client(
            auth=(settings.RAZORPAY_API_KEY, settings.RAZORPAY_API_SECRET)
            )

    def generate_payment_link(self, order_id, amount):
        #   order = self.client.order.create({"amount": amount, "currency": "INR", "payment_capture": "1"})
        #   return order["short_url"]
        payment_data = {
            "amount": amount,
            "currency": "INR",
            "description": "For XYZ purpose",
            "customer": {
                "name": "karan ",
                "email": "karan.bhatia_1@scaler.com",
                "contact": "+918295053001"
            },
            "notify": {
                "sms": True,
                "email": True
            },
            "reminder_enable": True,
            "callback_url": "https://google.com/",
            "callback_method": "get"
        }

        payment_link = self.client.payment_link.create(payment_data)
        return json.dumps(payment_link)
    
class StripePaymentGateway(PaymentGateway):
    def __init__(self):
        pass
    
    def generate_payment_link(self, order_id, amount):
        pass