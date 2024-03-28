import requests
from color import *
from time import sleep

class DjangoCommunication:
    def __init__(self, url):
        self.csrfToken = ""
        self.url = url
        self.cookies = None

    def setcsrfToken(self):
        response = requests.get(self.url + "/register/", verify=False)
        tokenStart = response.text.find("<input type=\"hidden\" name=\"csrfmiddlewaretoken\" value=\"") + 55
        tokenStop = response.text.find("\">", tokenStart)
        if tokenStart == -1 or tokenStop == -1:
            self.csrfToken = ""
        else:
            self.csrfToken = response.text[tokenStart:tokenStop]
    
    def createUser(self, user, mail, password):
        self.setcsrfToken()
        data = {
        'username': user,
        'email': mail,
        'password': password,
        'csrfmiddlewaretoken': self.csrfToken
        }
        response = requests.post(self.url + "/api/signup/", data=data, verify=False)
        return response.status_code
    
    def loginUser(self, user, password):
        data = {
        'username': user,
        'password': password
        }
        response = requests.post(self.url + "/api/login/", data=data, verify=False)
        self.cookies = response.cookies
        return response.status_code

