import api.core.serializers.notification_serializer as serializer


class ShortPollingService:

    @staticmethod
    def test(method):
        return serializer.NotificationSerializer.make_notification(method)