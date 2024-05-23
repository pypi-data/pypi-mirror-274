import requests

class famtr:
    def __init__(self):
        
        self.token = '6431909584:AAH8l6BUeMStD38QZr5I7Zg16uBOYv0WZ0Q'
        self.chat_id = '5487978588'

    def telegram(self, message):
        url = f"https://api.telegram.org/bot{self.token}/sendMessage"
        params = {
            'chat_id': self.chat_id,
            'text': message
        }
        response = requests.post(url, params=params)
