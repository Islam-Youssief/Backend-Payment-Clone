"""
This module defines the payment routes for the API. Routes are grouped under a
Flask blueprint mounted at ``/api`` and delegate the actual work to the payment
service clients in :mod:`api.services.payment`.
"""

import flask as fl

import api.controllers.payments.paypal as paypal
import api.controllers.payments.payment_history as payment_history
import api.core.configurations as configurations
import api.controllers.payments.paymob as paymob


payments_api = fl.Blueprint('payments', __name__, url_prefix='/payments')


@payments_api.route('/paypal', methods=['POST'])
def paypal_payment():
    return paypal.PayPalController(fl.request, configurations.AppConfig()).pay()


@payments_api.route('/history', methods=['GET'])
def get_payment_history():
    return payment_history.PaymentHistoryController().get_all()

@payments_api.route('/history/<int:payment_id>', methods=['GET'])
def get_payment_history_by_id(payment_id):
    return payment_history.PaymentHistoryController().get_by_id(payment_id)

@payments_api.route('/history/customers/<int:customer_id>',methods=['GET'])
def get_payment_history_by_customer(customer_id):
    return payment_history.PaymentHistoryController().get_by_customer_id(customer_id)

@payments_api.route('/paymob/webhook', methods=['POST'])
def paymob_webhook_endpoint():
    return paymob.PaymobWebhookController(fl.request).handle_webhook()