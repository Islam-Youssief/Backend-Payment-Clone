import requests
import api.core.configurations as config

class WaSenderService:

    @staticmethod
    def _send_message(phone,message):
        url = (f"{config.WaConfig.api_url}/api/send-message")

        headers = {
            "Authorization" : f"Bearer {config.WaConfig.api_key}",
            "Content-Type" : "application/json"
        }

        data = { 
            "to": f"{phone}", #Missing country code 
            "text": message
        }

        response = requests.post(url,headers=headers,json=data)
        
        response.raise_for_status()

        return response.json()

    @staticmethod
    def send_password_reset_otp(phone, otp):

        message = (
            f"""Your password reset OTP is: {otp}
            This code expires in 5 minutes."""
        )

        return WaSenderService._send_message(phone,message)
