"""
This module defines the payment routes for the API. Routes are grouped under a
Flask blueprint mounted at ``/api`` and delegate the actual work to the payment
service clients in :mod:`api.services.payment`.
"""

import flask as fl

import api.controllers.payments.paypal as paypal
import api.core.configurations as configurations
import api.controllers.payments.fawry as fawry
import api.controllers.payments.history as history

payments_api = fl.Blueprint('payments', __name__, url_prefix='/payments')


@payments_api.route('/paypal', methods=['POST'])
def paypal_payment():
    return paypal.PayPalController(fl.request, configurations.AppConfig()).pay()

@payments_api.route('/fawry', methods=['POST'])
def fawry_payment():
    return fawry.FawryController(fl.request, configurations.AppConfig()).pay()

@payments_api.route('/customer/<string:customer_id>', methods=['GET'])
def get_customer_payments(customer_id):
    return history.CustomerPaymentsController(fl.request).get(customer_id)

@payments_api.route('/<string:payment_id>', methods=['GET'])
def get_payment_detail(payment_id):
    return history.SinglePaymentController(fl.request).get(payment_id)
