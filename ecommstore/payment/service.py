from ecommstore.payment.gateways.payment_gateways import RazorpayPaymentGateway, StripePaymentGateway

class PaymentService:
    def __init__(self):
        self.payment_gateway = RazorpayPaymentGateway()

    def initiate_payment(self, order_id, amount):
        return self.payment_gateway.generate_payment_link(order_id, amount)