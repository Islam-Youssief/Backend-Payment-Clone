"""
This module defines the payment routes for the API. Routes are grouped under a
Flask blueprint mounted at ``/api`` and delegate the actual work to the payment
service clients in :mod:`api.services.payment`.
"""

import flask as fl

import api.controllers.payments.paypal as paypal
import api.controllers.payments.stripe as stripe
import api.core.configurations as configurations
import api.controllers.payments.login as login
import api.controllers.payments.payment_history as payment_history


payments_api = fl.Blueprint('payments', __name__, url_prefix='/payments')


@payments_api.route('/paypal', methods=['POST'])
def paypal_payment():
    return paypal.PayPalController(fl.request, configurations.AppConfig()).pay()

@payments_api.route('/stripe', methods=['POST'])
def stripe_payment():
    return stripe.StripeController(fl.request, configurations.AppConfig()).pay()

@payments_api.route('/login', methods=['POST'])
def stripe_login():
    return login.LoginController(fl.request, configurations.AppConfig()).login()

@payments_api.route('/<int:payment_id>', methods=['GET'])
def get_payment(payment_id):
    return payment_history.PaymentsHistoryController(
        fl.request,
        configurations.AppConfig()
    ).get_payment(payment_id)

@payments_api.route("/customer/<int:customer_id>", methods=["GET"])
def get_customer_payments(customer_id):
    return payment_history.PaymentsHistoryController(
        fl.request,
        configurations.AppConfig()
    ).get_customer_payments(customer_id)