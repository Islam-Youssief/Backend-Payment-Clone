import json
import time
import api.core.serializers.notification_serializer as serializer


class SSEService:

    @staticmethod
    def stream(method):

        for _ in range(5):
            time.sleep(2)

            notification = (serializer.NotificationSerializer.make_notification(method))


            yield (
                "event: notification\n"
                f"data: {json.dumps(notification)}\n\n"
            )
        yield (
            "event: complete\n"
            "data: {}\n\n"
        )