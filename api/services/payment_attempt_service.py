from typing import List, Optional
from uuid import UUID
from api.models import db
from api.models.payment_attempt import PaymentAttempt


class PaymentAttemptService:

    def create_payment_attempt(self, customer_id: UUID, provider: str, amount: float,
                               customer_name: str, customer_email: str, idempotency_key: UUID,
                               currency: str = 'EGP', status: str = 'PENDING') -> PaymentAttempt:
        """Create and persist a new PaymentAttempt record."""
        attempt = PaymentAttempt(
            customer_id=customer_id,
            provider=provider,
            amount=amount,
            currency=currency,
            status=status,
            customer_name=customer_name,
            customer_email=customer_email,
            idempotency_key=idempotency_key
        )
        db.session.add(attempt)
        db.session.commit()
        return attempt

    def get_payment_attempt_by_id(self, payment_id: UUID) -> Optional[PaymentAttempt]:
        """Fetch a PaymentAttempt by primary key UUID."""
        return db.session.get(PaymentAttempt, payment_id)

    def get_payment_attempt_by_idempotency_key(self, idempotency_key: UUID) -> Optional[PaymentAttempt]:
        """Fetch a PaymentAttempt by idempotency_key UUID."""
        return PaymentAttempt.query.filter_by(idempotency_key=idempotency_key).first()

    def get_payment_attempts_by_customer_id(self, customer_id: UUID) -> List[PaymentAttempt]:
        """Fetch all payment attempts associated with a customer_id."""
        return PaymentAttempt.query.filter_by(customer_id=customer_id).all()

    def update_payment_attempt_status(self, payment_id: UUID, status: str, provider_reference: Optional[str] = None,
                                      failure_reason: Optional[str] = None) -> Optional[PaymentAttempt]:
        """Update the status and provider info of a PaymentAttempt."""
        attempt = self.get_payment_attempt_by_id(payment_id)
        if not attempt:
            return None
        attempt.status = status
        if provider_reference:
            attempt.provider_reference = provider_reference
        if failure_reason:
            attempt.failure_reason = failure_reason
        db.session.commit()
        return attempt

    def delete_payment_attempt(self, payment_id: UUID) -> bool:
        """Delete a PaymentAttempt record by ID."""
        attempt = self.get_payment_attempt_by_id(payment_id)
        if not attempt:
            return False
        db.session.delete(attempt)
        db.session.commit()
        return True
