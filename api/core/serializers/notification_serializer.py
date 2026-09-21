import time
class NotificationSerializer:

    @staticmethod
    def make_notification(method):
        sent_at = time.time_ns()
        return {
            "id": sent_at,
            "method": method,
            "message": f"Test notification from {method}",
            "sent_at": sent_at // 1_000_000,
        }