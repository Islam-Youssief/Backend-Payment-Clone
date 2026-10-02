import flask as fl
from api.services.trello import create_trello_card
from api.services.notifications.error_reporting import ErrorReportingService
from api.services.notifications.notification_counter import NotificationCounter
from api.services.authentication.email import EmailService
import api.core.configurations as config
import asyncio
class TrelloController:

    @staticmethod
    def create_card():
        data = fl.request.get_json()
        name = data.get("name")
        desc = data.get("desc")

        if not name or not desc:
            return {
                "msg": "Missing name and desc"
            }, 400

        create_trello_card(name,desc)

        return {
            "msg": "Card created successfully"
        }, 201
    
    @staticmethod
    async def error_trello():
        data = fl.request.get_json() or {}
        error_level = data.get("error_level", "warning")
        try:
            raise RuntimeError("Test error")
        except Exception as exception:
            
            result = ErrorReportingService.report(exception)
            if error_level == "critical" :
                emailService = EmailService()
                email = config.SmtpConfig.smtp_log_email
                await asyncio.to_thread(emailService.send_error,
                email,error_level,
                result["exception"],
                result["traceback"]
                )
                    
                error_method = "Error Trello + Email"
            NotificationCounter.increment_error_trello()
            return {
                "success": True,
                "method": "Error Trello",
                "message": result["exception"]
            }, 200
    
    def get_error_count():
        count = NotificationCounter.get_error_trello()

        return {
            "notification_count": count
        }, 200