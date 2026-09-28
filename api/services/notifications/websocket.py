import json
import time

import api.core.serializers.notification_serializer as serializer

class WebSocketService:
    @staticmethod
    def sent_test(ws , method):
        for _ in range(5):
            time.sleep(2)
            notification = serializer.NotificationSerializer.make_notification(method)
            ws.send(json.dumps(notification))