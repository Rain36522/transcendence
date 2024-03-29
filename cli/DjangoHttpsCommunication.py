import requests
from color import *
from time import sleep

class DjangoCommunication:
    def __init__(self):
        self.csrfToken = ""
        self.url = None
        self.wsUrl = None
        self.cookies = None

    def setWsUrl(self, username, gameid):
        url = self.url.split("/")
        self.wsUrl = "wss://" + url[2] + "/wsGame/" + username + "/" + str(gameid)

    def CheckUrl(self, url):
        try:
            response = requests.get(url + "/register/", verify=False)
            if response.status_code == 200:
                self.url = url
        except:
            return 500
        return response.status_code

    def setcsrfToken(self):
        try:
            response = requests.get(self.url + "/register/", verify=False)
        except:
            return 500
        tokenStart = response.text.find("<input type=\"hidden\" name=\"csrfmiddlewaretoken\" value=\"") + 55
        tokenStop = response.text.find("\">", tokenStart)
        if tokenStart == -1 or tokenStop == -1:
            self.csrfToken = ""
            return 404
        else:
            self.csrfToken = response.text[tokenStart:tokenStop]
            return 200
    
    def createUser(self, user, mail, password):
        value = self.setcsrfToken()
        if value != 200:
            return value
        data = {
        'username': user,
        'email': mail,
        'password': password,
        'csrfmiddlewaretoken': self.csrfToken
        }
        try:
            response = requests.post(self.url + "/api/signup/", data=data, verify=False)
            return response.status_code
        except:
            return 500
    
    def loginUser(self, user, password):
        data = {
        'username': user,
        'password': password
        }
        try:
            response = requests.post(self.url + "/api/login/", data=data, verify=False)
            self.cookies = response.cookies
            return response.status_code
        except:
            return 500

