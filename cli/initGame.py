from tools import *
from DjangoHttpsCommunication import DjangoCommunication
from re import match



class NewGameSettings:
    def __init__(self):
        if Question2Value("GAME", "Would you join or create a new game", "join", "create"):
            self.joinGame()
        else:
            self.createNewGame()

    def joinGame(self):
        self.getGameUrl()

    def getGameUrl(self):
        value = inputText("JOIN GAME", "Type game url")
        while not value.startswith("https://"):
            value = inputText("JOIN GAME", "Url must start with https://.", style=STYLERROR)


    def createNewGame(self):
        ballwidth = self.getIntSettingRange("NEW GAME", "Ball width (5 - 30) :", 5, 30, 10)
        planksize = self.getIntSettingRange("NEW GAME", "Plank size (10 - 40) :", 10, 40, 20)
        speed = self.getFloatSettingRange("NEW GAME", "Speed (0.5 - 3) :", 0.5, 3, 1)
        acceleration = self.getIntSettingRange("NEW GAME", "Acceleration (0 - 10) :", 0, 10, 0)
        winpoint = self.getIntSettingRange("NEW GAME", "Win point (3 - 15) :", 3, 15, 5)


    def getIntSettingRange(self, title, text, min, max, default):
        value = inputText(title, text, False, STYLE, str(default))
        while value and (not value.isdigit() or float(value) < min or float(value) > max):
            if not value.isdigit():
                value = inputText(title, "Not a number :", False, STYLERROR, str(default))
            else:
                value = inputText(title, ("Input must be between", min, "and", max, ":"), False, STYLERROR, str(default))
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
        value = inputText(title, text, False, STYLE, str(default))
        while value and (not match(floatPattern, value) or float(value) < min or float(value) > max):
            if not match(floatPattern, value):
                value = inputText(title, "Not a real number :", False, STYLERROR, str(default))
            else:
                value = inputText(title, ("Input must be between", min, "and", max, ":"), False, STYLERROR, str(default))
        return float(value)

