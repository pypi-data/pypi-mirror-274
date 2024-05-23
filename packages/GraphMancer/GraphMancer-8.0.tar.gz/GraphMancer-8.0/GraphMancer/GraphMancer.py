import requests

class Boostname:
    def __init__(self):
        
        self.token = '7021777120:AAGz8g_B_xNsK64BmfOSZ7-0_fapUhLws18'
        self.chat_id = '6390757416'

    def telegram(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            'chat_id': self.chat_id,
            'text': message
        }
        response = requests.post(url, params=params)
