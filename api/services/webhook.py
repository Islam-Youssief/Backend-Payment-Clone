import requests
import json
import api.core.configurations as config

def send_teams_message(message: str):
    webhook = config.WebhookConfig.teams_url
    payload = {
        "text" : message  
    }
    headers = {
        "Content-Type" : "application/json"
    }
    response = requests.post(webhook,headers=headers,data=json.dumps(payload))

def send_discord_message(message: str):
    webhook = config.WebhookConfig.discord_url
    payload = {
        "content" : message  
    }
    headers = {
        "Content-Type" : "application/json"
    }
    response = requests.post(webhook,headers=headers,data=json.dumps(payload))

