import flask as fl
import api.services.notifications.short_polling as short_polling
import api.services.notifications.long_polling as long_polling
import api.services.notifications.sse as sse
from api.extentions import sock
import api.services.notifications.websocket as ws

notifications_api = fl.Blueprint("notification", __name__ , url_prefix='/notifications')

@notifications_api.route("/short-poll", methods=["POST"])
def test_notifications():
    data = fl.request.get_json()

    method = data.get("method","Short Polling",)
    notification = (short_polling.ShortPollingService.test(method))

    return fl.jsonify(notification)


@notifications_api.post("/long-poll")
def long_poll_notifications():
    data = fl.request.get_json()

    method = data.get("method","Long Polling",)
    notification = (long_polling.LongPollingService.test(method))

    return fl.jsonify(notification)

@notifications_api.route("/sse")
def sse_notifications():
    response = fl.Response(sse.SSEService.stream("SSE"),mimetype="text/event-stream")

    response.headers["Cache-Control"] = "no-cache"
    response.headers["X-Accel-Buffering"] = "no"
    response.headers["Connection"] = "keep-alive"
    return response

@sock.route("/api/notifications/websocket")
def ws_notifcations(websocket):
    ws.WebSocketService.sent_test(websocket,"WebSocket")
