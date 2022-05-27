import requests

class Api:
    def __init__(self):
        self.HOST = 'http://127.0.0.1:8000'
        self.main_link = f'{self.HOST}/json_simple'
    
    def get_all_todos(self):
        r = requests.get(self.main_link)
        return r.json()