from re import match
from tools import *
from DjangoHttpsCommunication import DjangoCommunication


class User:
    def __init__(self, Django):
        self.username = ""
        self.userToken = None
        self.Django = Django
        if Question2Value("MAIN", "Login or signup?", "LOGIN", "signup"):
            self.doLogin()
        else:
            self.doRegistration()
        
    def doLogin(self):
        user, pwd = self.login()
        value = self.Django.loginUser(user, pwd)
        while value != 200 and value != 500:
            result = Question3Value("LOGIN", "Login fail.", "Retry", "signup", "exit", style=STYLERROR)
            if result == 1:
                user, pwd = self.login(error=True)
                value = self.Django.loginUser(user, pwd)
            elif result == 0:
                self.doRegistration()
                return
            else:
                doexit(1)
        if value == 500:
                doexit(1, "Error: Serveur not accessible.")
        Information("LOGIN", "User connection succes.", style=STYLSUCCESS)
        

    def login(self, error=False):
        if error:
            user = inputText("LOGIN", "Wrong login. User : ", False, STYLERROR)
            pwd = inputText("LOGIN", "Wrong login. password : ", True, STYLERROR)
        else:
            user = inputText("LOGIN", "Please type your username: ")
            pwd = inputText("LOGIN", "Please type your password: ", True)
        return user, pwd

    def doRegistration(self):
        user, mail, pwd = self.registration()
        value = self.Django.createUser(user, mail, pwd)
        while value != 200 and value != 500:
            result = Question3Value("REGISTRATION", "User or email already existing.", "signup", "login", "exit", style=STYLERROR)
            if result == 0:
                self.doLogin()
                return
            elif result == -1:
                doexit(1)
            user, mail, pwd = self.registration()
            value = self.Django.createUser(user, mail, pwd)
        if value == 500:
                doexit(1, "Error: Serveur not accessible.")
        Information("SIGNUP", "User creation succes.", style=STYLSUCCESS)

    def registration(self):
        user = inputText("REGISTRATION", "Username :")
        mail = self.getMail()
        pwd = self.getPwd()
        return user, mail, pwd


    def getMail(self, error=False):
        mailPattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        inputmsg = "E-mail :"
        mail = inputText("REGISTRATION", inputmsg)
        while mail and not match(mailPattern, mail):
            inputmsg = "Wrong mail, Try again :"
            mail = inputText("SIGNUP", inputmsg, False, STYLERROR)
        return mail

    def getPwd(self):
        text1 = "Type password :"
        text2 = "Confirm password :"
        pwd1 = inputText("SIGNUP", text1, True)
        pwd2 = inputText("SIGNUP", text2, True)
        while not pwd1 or pwd1 != pwd2:
            if not pwd1:
                text1 = "No password write :"
            else:
                text1 = "Password not corresponding :"
            pwd1 = inputText("SIGNUP", text1, True, STYLERROR)
            pwd2 = inputText("SIGNUP", text2, True, STYLERROR)
        return pwd1
