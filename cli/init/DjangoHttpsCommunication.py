import sys
import os
chemin_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(chemin_parent)
import requests
from color import *
from time import sleep
from os import system

class DjangoCommunication:
    def __init__(self):
        self.csrfToken = ""
        self.url = None
        self.wsUrl = None
        self.cookies = None
        system("clear")

    def setWsUrl(self, username, gameid):
        url = self.url.split("/")
        self.wsUrl = "wss://" + url[2] + "/wsGame/" + username + "/" + str(gameid)

    def CheckUrl(self, url):
        try:
            response = requests.get(url + "/register/", verify=False)
        except:
            return 500
        if  response.text.find("<input type=\"hidden\" name=\"csrfmiddlewaretoken\" value=\"") >= 0:
            self.url = url
            return response.status_code
        return 500

    def setcsrfToken(self):
        try:
            response = requests.get(self.url + "/register/", verify=False)
        except:
            return 500
        system("clear")
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
            system("clear")
            self.cookies = response.cookies
            return response.status_code
        except:
            return 500
    
    def loginUser(self, user, password):
        data = {
        'username': user,
        'password': password
        }
        try:
            print("65")
            response = requests.post(self.url + "/api/login/", data=data, verify=False)
            print("67")
            self.cookies = response.cookies
            system("clear")
            return response.status_code
        except:
            return 500

    def createGame(self):
        pass
