from prompt_toolkit.shortcuts import message_dialog
from prompt_toolkit.shortcuts import button_dialog
from prompt_toolkit.shortcuts import input_dialog
from prompt_toolkit.styles import Style
from re import match

style = Style.from_dict({
    'dialog':             'bg:#202020',
    'dialog frame.label': 'bg:#353535 #cccccc',
    'dialog.body':        'bg:#303030 #bbbbbb',
    'dialog shadow':      'bg:#202020',
})

styleError = Style.from_dict({
    'dialog':             'bg:#202020',
    'dialog frame.label': 'bg:#353535 #cccccc',
    'dialog.body':        'bg:#303030 #ff0000',
    'dialog shadow':      'bg:#202020',
})

def Question3Value(title, text, value1, value2, value3):
    return button_dialog(
        title=title,
        text=text,
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
        style=style,
        buttons=[
            (value1, True),
            (value2, False),
        ]
    ).run()

def inputText(title, text, password=False, style=style):
    return input_dialog(
    title=title,
    text=text,
    password=password,
    style=style).run()

def login(error=False):
    if error:
        user = inputText("LOGIN", "Wrong login. User : ", False, styleError)
        pwd = inputText("LOGIN", "Wrong login. password : ", True, styleError)
    else:
        user = inputText("LOGIN", "Please type your username: ")
        pwd = inputText("LOGIN", "Please type your password: ", True)
    return user, pwd

def registration():
    user = inputText("REGISTRATION", "Username :")
    mail = getMail()
    pwd = getPwd()
    return user, mail, pwd


def getMail():
    mailPattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    inputmsg = "E-mail :"
    mail = inputText("REGISTRATION", inputmsg)
    while not match(mailPattern, mail):
        inputmsg = "Wrong mail, Try again :"
        mail = inputText("REGISTRATION", inputmsg, False, styleError)
    return mail

def getPwd():
    text1 = "Type password :"
    text2 = "Confirm password :"
    pwd1 = inputText("REGISTRATION", text1, True)
    pwd2 = inputText("REGISTRATION", text2, True)
    while not pwd1 or pwd1 != pwd2:
        if not pwd1:
            text1 = "No password write :"
        else:
            text1 = "Password not corresponding :"
        pwd1 = inputText("REGISTRATION", text1, True, styleError)
        pwd2 = inputText("REGISTRATION", text2, True, styleError)
    return pwd1

def joinGame():
    return inputText("Join game", "Select an valide url!")
    
def createGame():
    pass


def getIntSettingRange(self, min, max, str):
    result = min - 1
    while result < min or result > max:
        value = input(str)
        if value.isdigit():
            result = int(value)
        if not value.isdigit():
            print(ORANGE, "The input accept only digit.", RESET)
        elif result < min or result > max:
            print(ORANGE, "The value must be between", min, "and", str(max) + ".", RESET)

def getSetting(self, values, str):
    while True:
        value = input(str)
        if value in values:
            return value
        else:
            print("Wrong value input!")
            

def getFloatSettingRange(title, text, min, max):
    floatPattern = r'^\d+(\.\d+)?$'
    value = inputText(title, text)
    while not match(floatPattern, value) or float(value) < min or float(value) > max:
        if not match(floatPattern, value):
            value = inputText(title, "Not a real number :", False, styleError)
        else:
            value = inputText(title, ("Input must be betweene", min, "and", max, ":"), False, styleError)
    return float(value)


print(registration())