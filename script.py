
import api.services.payment.stripe as stripe
import  api.services.payment.paypal as paypal

client = paypal.PayPalClient('lcl')
response = client.pay_with_visa(data={"amount": 10.00, "currency": "EGP", "payment_method": "visa"})
print(response.json())


client = stripe.StripeClient('lcl')
response = client.create_payment_intent(data={"user_name": "Ahmed Mohammad Ali", "amount": "100", "visa_number": "4242424242424242","cvv":"123"})
print(response.json())







