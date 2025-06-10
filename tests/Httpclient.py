import requests

class Httpclient:
    def __init__(self, base_url):
        self.base_url = base_url
    def post(self, path, data, headers):
        url = self.base_url + path
        response = requests.post(url, json=data, headers=headers)
        return response
    def get(self, path, headers):
        url = self.base_url + path
        response = requests.get(url, headers=headers)
        return response

