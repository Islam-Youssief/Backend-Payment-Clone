import json
import os

class NotificationCounter:

    FILE_PATH = os.path.join(os.path.dirname(__file__),"../../core/notification_counter.json")

    @staticmethod
    def _read():

        with open(NotificationCounter.FILE_PATH,"r") as file:
            return json.load(file)

    @staticmethod
    def _write(data):

        with open(NotificationCounter.FILE_PATH,"w") as file:
            json.dump(data,file,indent=4)

    @staticmethod
    def increment_error_trello():

        data = NotificationCounter._read()

        data["error_trello"] += 1

        NotificationCounter._write(data)

        return data["error_trello"]

    @staticmethod
    def get_error_trello():

        data = NotificationCounter._read()

        return data["error_trello"]