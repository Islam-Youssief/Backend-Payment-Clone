import flask as fl
from api.controllers.trello import TrelloController

trello_api = fl.Blueprint("trello",__name__,url_prefix="/trello")


@trello_api.route("/create_card",methods=["POST"])
def create_card():
    return TrelloController.create_card()

@trello_api.route("/error_trello",methods=["POST"])
async def error_trello():
    return await TrelloController.error_trello()

@trello_api.route("/get_error_count",methods=["get"])
def error_count():
    return TrelloController.get_error_count()
