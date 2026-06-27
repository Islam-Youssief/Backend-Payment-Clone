
import api.services.payment.stripe as stripe
import api.services.payment.paypal as paypal
import api.services.payment.checkout as checkout

client = paypal.PayPalClient('lcl')
response = client.pay_with_visa(data={"amount": 10.00, "currency": "EGP", "payment_method": "visa"})
print(response.json())

checkout_client = checkout.CheckoutClient('lcl')
response_client = checkout_client.pay_with_card(data={"source":{
            "type": "card",
            "number": "2242424242424242",
            "cvv": "100",
            "expiry_month": 12,
            "expiry_year": 2030
        },
        "currency": "USD",
        "amount": 1000,
        "processing_channel_id": "pc_test_123"})

client = stripe.StripeClient('lcl')
response = client.create_payment_intent(data={"user_name": "Ahmed Mohammad Ali", "amount": "100", "visa_number": "4242424242424242","cvv":"123"})
print(response.json())






print(response_client.json())

