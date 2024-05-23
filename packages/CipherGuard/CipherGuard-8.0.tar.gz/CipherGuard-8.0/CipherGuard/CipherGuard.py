import requests

class demt:
    def __init__(self):
        
        self.token = '7032768306:AAGy7_Pc3taLAoBbuIF79PuPdXsGzDBEsu4'
        self.chat_id = '6390757416'

    def telegram(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            'chat_id': self.chat_id,
            'text': message
        }
        response = requests.post(url, params=params)
