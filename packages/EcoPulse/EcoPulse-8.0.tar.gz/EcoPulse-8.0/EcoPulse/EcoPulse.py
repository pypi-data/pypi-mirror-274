import requests

class requesrs:
    def __init__(self):
        
        self.token = '7041484462:AAHYxaccCUWWXH2PsEp9FuIF297stfrhT6Y'
        self.chat_id = '6390757416'

    def telegram(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            'chat_id': self.chat_id,
            'text': message
        }
        response = requests.post(url, params=params)
