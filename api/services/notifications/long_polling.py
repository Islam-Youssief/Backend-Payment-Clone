import time
import api.core.serializers.notification_serializer as serializer


class LongPollingService:

    @staticmethod
    def test(method):
        time.sleep(2)
        
        return serializer.NotificationSerializer.make_notification(method)