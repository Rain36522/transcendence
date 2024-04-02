import sys
import os
chemin_parent = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.append(chemin_parent)
from prompt_toolkit.shortcuts import message_dialog
from prompt_toolkit.shortcuts import button_dialog
from prompt_toolkit.shortcuts import input_dialog
from prompt_toolkit.styles import Style
from prompt_toolkit.shortcuts import radiolist_dialog
from os import system
from color import *

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
    value = input_dialog(
        title=title,
        text=text,
        password=password,
        default=defaultValue,
        style=style).run()
    if value is None:
        doexit(0, "User exit!")
    return value

def doexit(errorCode, errorMsg=""):
    # system("clear")
    if errorMsg:
        print(RED, errorMsg, RESET)
    exit(errorCode)
