import api.core.exceptions as exceptions


class MeezaPaymentDataValidator:

    REQUIRED_FIELDS = [
        "amount",
        "currency",
        "country",
        "payment_method_id",
        "payment_method_flow",
        "payer",
        "order_id",
        "description",
        "notification_url",
        "callback_url"
    ]

    def validate(self, data):
        self._validate_required_fields(data)
        self._validate_amount(data["amount"])
        self._validate_payment_method(data["payment_method_id"])
        self._validate_payment_flow(data["payment_method_flow"])

    def _validate_required_fields(self, data):
        missing_fields = [
            field
            for field in self.REQUIRED_FIELDS
            if field not in data
        ]

        if missing_fields:
            raise exceptions.RequiredInputError(
                f"Missing fields: {missing_fields}"
            )

    def _validate_amount(self, amount):
        try:
            amount = float(amount)
        except (ValueError, TypeError):
            raise exceptions.InputDataTypeError(
                message=f"Invalid amount type. Expected Decimal, Got: {type(amount).__name__}"
            )

        if amount <= 0:
            raise exceptions.ValidationError(
                message="Amount must be greater than zero"
            )

    def _validate_payment_method(self, payment_method):
        if payment_method != "EW":
            raise exceptions.ValidationError(
                message="Meeza payment_method_id must be EW"
            )

    def _validate_payment_flow(self, payment_flow):
        if payment_flow != "REDIRECT":
            raise exceptions.ValidationError(
                message="Meeza payment_method_flow must be REDIRECT"
            )