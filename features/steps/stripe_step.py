import os


from behave import given, then, when

from api.services.payment.stripe import StripeClient

@given("the Stripe API is available")
def step_stripe_payment_is_available(context):
    os.environ["STRIPE_SECRET_KEY"] = "STRIPE_SECRET_KEY"
    context.data = {
        "user_name": "Ahmed Mohammad Ali",
        "amount": 100,
        "visa_number":"4222422242224222",
        "cvv":"123"
    }
@given("the Stipe API declines the payment")
def step_decline_the_payment(context):
    context.data = {
        "user_name": "Ahmed Mohammad Ali",
        "amount": 100,
        "visa_number": "4000000000000001",
        "cvv": "123"
    }
@given("the Stripe API is unavailable")
def step_is_unavailable(context):
    context.data = {
        "user_name": "Ahmed Mohammad Ali",
        "amount": 100,
        "visa_number": "4000000000000000",
        "cvv": "123"
    }
@given("the Stripe secret key is missing")
def step_secret_key_is_missing(context):
    os.environ.pop("STRIPE_SECRET_KEY", None)
    context.data = {
        "user_name": "Ahmed Mohammad Ali",
        "amount": 100,
        "visa_number": "4222422242224222",
        "cvv": "123"
    }
@given("the Stripe secret key is invalid")
def step_secret_key_is_invalid(context):
    os.environ["STRIPE_SECRET_KEY"] ="Invalid_Secret_Key"
    context.data = {
        "user_name": "Ahmed Mohammad Ali",
        "amount": 100,
        "visa_number": "4222422242224222",
        "cvv": "123"
    }
@given("the Stripe API is rate limiting requests")
def step_request_rate_limiting_request(context):
    os.environ["STRIPE_SECRET_KEY"] = "STRIPE_SECRET_KEY"
    context.data = {
        "user_name": "Ahmed Mohammad Ali",
        "amount": 100,
        "visa_number": "4294294294294294",
        "cvv": "123"
    }

@when("the customer creates a payment")
def step_customer_create_payment(context):
    client = StripeClient("lcl")
    context.response = client.create_payment_intent(context.data)

@then('the response status code is equal to {status_code:d}')
def step_response_status_code(context, status_code):
    print(context.response.status_code)
    print(context.response.text)
    assert context.response.status_code ==status_code

@then('the response message is equal to "{message}"')
def step_response_message(context, message):
    assert context.response.json()['message'] == message

