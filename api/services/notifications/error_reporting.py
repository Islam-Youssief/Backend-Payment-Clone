import traceback
from api.services.webhook import send_discord_message
from api.services.trello import create_trello_card

class ErrorReportingService:

    @staticmethod
    def report(exception):
        exception_name = type(exception).__name__
        traceback_text = traceback.format_exc()

        send_discord_message(f"```Exception: {exception_name}\n {traceback_text}```")
        trello_card = create_trello_card(exception_name,traceback_text)
        return {
            "exception": exception_name,
            "traceback": traceback_text,
            "trello": trello_card
        }