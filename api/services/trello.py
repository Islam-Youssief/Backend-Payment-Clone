import api.core.configurations as config
import requests

def create_trello_card(name,description):
    payload = {
        'idBoard': config.WebhookConfig.trello_board,
        "idList": config.WebhookConfig.trello_list,
        "name" : name,
        "desc" : description
    }
    params = {
        "key": config.WebhookConfig.trello_api_key,
        "token": config.WebhookConfig.trello_token,
    }
   
    response = requests.post(config.WebhookConfig.trello_url,params=params,json=payload)

