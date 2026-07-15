"""
This module defines the payment routes for the API. Routes are grouped under a
Flask blueprint mounted at ``/api`` and delegate the actual work to the payment
service clients in :mod:`api.services.payment`.
"""

import flask as fl

import api.controllers.payments.checkout as checkout
import api.controllers.payments.paypal as paypal
import api.core.configurations as configurations


payments_api = fl.Blueprint('payments', __name__, url_prefix='/payments')


@payments_api.route('/paypal', methods=['POST'])
def paypal_payment():
    return paypal.PayPalController(fl.request, configurations.AppConfig()).pay()

@payments_api.route('/checkout', methods=['POST'])
def checkout_payment():
    return checkout.CheckoutController(fl.request, configurations.AppConfig()).pay()

