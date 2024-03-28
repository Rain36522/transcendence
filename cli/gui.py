from prompt_toolkit.shortcuts import message_dialog
from prompt_toolkit.shortcuts import button_dialog
from prompt_toolkit.shortcuts import input_dialog
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import radiolist_dialog
import DjangoHttpsCommunication as DjangoServ
from DjangoHttpsCommunication import DjangoCommunication
from re import match
from os import system

STYLE = Style.from_dict({
    'dialog':             'bg:#202020',
    'dialog frame.label': 'bg:#353535 #cccccc',
    'dialog.body':        'bg:#303030 #bbbbbb',
    'dialog shadow':      'bg:#202020',
})

STYLERROR = Style.from_dict({
    'dialog':             'bg:#202020',
    'dialog frame.label': 'bg:#353535 #cccccc',
    'dialog.body':        'bg:#303030 #ff0000',
    'dialog shadow':      'bg:#202020',
})
STYLSUCCESS = Style.from_dict({
    'dialog':             'bg:#202020',
    'dialog frame.label': 'bg:#353535 #cccccc',
    'dialog.body':        'bg:#303030 #00ff00',
    'dialog shadow':      'bg:#202020',
})

def Information(title, text, style=STYLE):
    message_dialog(title=title, text=text, style=style).run()

def Question3Value(title, text, value1, value2, value3, style=STYLE):
    return button_dialog(
        title=title,
        text=text,
        style=style,
        buttons=[
            (value1, 1),
            (value2, 0),
            (value3, -1)
        ]
    ).run()

def Question2Value(title, text, value1, value2):
    return button_dialog(
        title=title,
        text=text,
        style=STYLE,
        buttons=[
            (value1, True),
            (value2, False),
        ]
    ).run()

def inputText(title, text, password=False, style=STYLE, defaultValue=""):
    return input_dialog(
        title=title,
        text=text,
        password=password,
        default=defaultValue,
        style=style).run()

def doexit(errorCode):
    system("clear")
    exit(errorCode)

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
        while self.Django.loginUser(user, pwd) != 200:
            result = Question3Value("LOGIN", "Login fail.", "Retry", "signup", "exit", style=STYLERROR)
            if result == 1:
                self.login(error=True)
            elif result == 0:
                self.doRegistration()
                return
            else:
                doexit(1)
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
        while self.Django.createUser(user, mail, pwd) != 200:
            result = Question3Value("REGISTRATION", "User already existing.", "signup", "login", "exit", style=STYLERROR)
            if result == 0:
                self.doLogin()
                return
            elif result == -1:
                doexit(1)
            else:
                user, mail, pwd = self.registration()
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


class GameStart:
    def __init__(self):
        self.wssUrl = ""
        self.httpsUrl = ""


class NewGameSettings:
    def __init__(self):
        ballwidth = self.getIntSettingRange("NEW GAME", "Ball width (5 - 30) :", 5, 30, 10)
        planksize = self.getIntSettingRange("NEW GAME", "Plank size (10 - 40) :", 10, 40, 20)
        speed = self.getFloatSettingRange("NEW GAME", "Speed (0.5 - 3) :", 0.5, 3, 1)
        acceleration = self.getIntSettingRange("NEW GAME", "Acceleration (0 - 10) :", 0, 10, 0)
        winpoint = self.getIntSettingRange("NEW GAME", "Win point (3 - 15) :", 3, 15, 5)


    def getIntSettingRange(self, title, text, min, max, default):
        value = inputText(title, text, False, STYLE, default)
        while value and (not value.isdigit() or float(value) < min or float(value) > max):
            if not value.isdigit():
                value = inputText(title, "Not a number :", False, STYLERROR, default)
            else:
                value = inputText(title, ("Input must be between", min, "and", max, ":"), False, STYLERROR, default)
        return int(value)

    def getSetting(self, title, text, values):
        listValues = []
        i = 0
        for value in values:
            listValues.append((i, value))
            i += 1
        return radiolist_dialog(
            title=title,
            text=text,
            values=listValues,
            style=STYLE).run

    def getFloatSettingRange(self, title, text, min, max, default):
        floatPattern = r'^\d+(\.\d+)?$'
        value = inputText(title, text, False, STYLE, default)
        while value and (not match(floatPattern, value) or float(value) < min or float(value) > max):
            if not match(floatPattern, value):
                value = inputText(title, "Not a real number :", False, STYLERROR, default)
            else:
                value = inputText(title, ("Input must be between", min, "and", max, ":"), False, STYLERROR, default)
        return float(value)


Django = DjangoCommunication("https://127.0.0.1")
User(Django)
