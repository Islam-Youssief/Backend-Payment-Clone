import flask as fl

import api.controllers.images as images
import api.controllers.transactions as transactions

from api.services.authentication.decorator import require_authentication
from api.services.permissions import PermissionService

dashboard_api = fl.Blueprint("dashboard",__name__,url_prefix="/payments")

@dashboard_api.route("/images", methods=["GET"])
@require_authentication
def get_images(user):
    if not PermissionService.has_permission(user.id,"gallery_allowed"):
        return {
            "message": "You do not have permission to access the gallery"
        }, 403

    limit = fl.request.args.get("limit",2,type=int)

    cursor = fl.request.args.get("cursor",type=int)

    limit = min(max(limit, 1), 100)

    return images.ImageController.get_images(limit=limit,cursor=cursor)


@dashboard_api.route("/transactions/customer/<int:customer_id>",methods=["GET"])
@require_authentication
def get_transactions(user, customer_id):
    if not PermissionService.has_permission(user.id,"transactions_allowed"):
        return {
            "message": "You do not have permission to access transactions"
        }, 403

    return transactions.TransactionController.get_by_customer_id(customer_id)


@dashboard_api.route("/transactions/customer/<int:customer_id>/summary",methods=["GET"])
@require_authentication
def get_transaction_summary(user, customer_id):
    if not PermissionService.has_permission(user.id,"transactions_allowed"):
        return {
            "message": "You do not have permission to access transactions"
        }, 403

    return transactions.TransactionController.get_spending_by_category(customer_id)