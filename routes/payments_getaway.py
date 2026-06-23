import threading

from flask import Blueprint, request, jsonify

from api.services.payment.mezza import MezzaPaymentService


payments_bp = Blueprint("payments", __name__)
service = MezzaPaymentService(env='lcl')


@payments_bp.route("/payments", methods=["POST"])
def create():
    payment = service.create_payment(request.json)
    threading.Thread(target=service.async_finalize, args=(payment["id"],)).start()
    return jsonify(payment), 201


@payments_bp.route("/payments/<payment_id>", methods=["GET"])
def get(payment_id):
    payment = service.get_payment(payment_id)
    if not payment:
        return jsonify({"error": "Not found"}), 404
    return jsonify(payment)


@payments_bp.route("/mock/pay/<payment_id>", methods=["GET"])
def mock_pay_page(payment_id):
    payment = service.get_payment(payment_id)
    if not payment:
        return "Payment not found", 404

    return f"""
    <h2>Mock Payment Gateway</h2>
    <p>Amount: {payment['amount']} {payment['currency']}</p>
    <p>Status: {payment['status']}</p>

    <form action="/mock/pay/{payment_id}/success" method="post">
        <button>Pay</button>
    </form>

    <form action="/mock/pay/{payment_id}/fail" method="post">
        <button>Fail</button>
    </form>
    """


@payments_bp.route("/mock/pay/<payment_id>/success", methods=["POST"])
def success(payment_id):
    return jsonify(service.mark_paid(payment_id))


@payments_bp.route("/mock/pay/<payment_id>/fail", methods=["POST"])
def fail(payment_id):
    return jsonify(service.mark_failed(payment_id))
