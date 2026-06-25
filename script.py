
import api.services.payment.paypal as paypal


client = paypal.PayPalClient('lcl')
response = client.pay_with_visa(data={"amount": 10.00, "currency": "EGP", "payment_method": "visa"})
print(response.json())







