



class CoreErrorSerializer:
    def __init__(self, error, status):
        self._error = error
        self._status = status

    def serialize(self, path):
        return {
            "path": path,
            "status": self._status,
            "description": self._status.phrase,
            "message": self._error.message,
            "data": self._error.data
        }
