from abc import ABC, abstractmethod
import razorpay
import json
from ecommstore import settings
from pprint import pprint
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
        amount = int(amount * 100) # converting to paise
        
        payment_data = {
            "amount": amount,
            "currency": "INR",
            "description": "Demo Payment Description",
            "customer": {
                "name": "Dushyant Baweja",
                "email": "dbaweja@gmail.com",
                "contact": "+919889883874"
            },
            "notify": {
                "sms": True,
                "email": True
            },
            "reminder_enable": True,
            "callback_url": "https://google.com/",
            "callback_method": "get"
        }

        pprint("Creating payment link with: " +str(payment_data))
        try:
            payment_link = self.client.payment_link.create(payment_data)
        except Exception as e:
            pprint(f"An error occurred while creating payment link: {e}")
            return json.dumps({"error": "An error occurred while creating payment link."})
        
        pprint("payment link is created.")
        return json.dumps(payment_link)
    
class StripePaymentGateway(PaymentGateway):
    def __init__(self):
        pass
    
    def generate_payment_link(self, order_id, amount):
        pass