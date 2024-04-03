from tools import *
from DjangoHttpsCommunication import DjangoCommunication
from re import match



class NewGameSettings:
    def __init__(self):
        termSize = os.get_terminal_size()
        if termSize.columns < 80 or termSize.lines < 20:
            while termSize.columns < 80 or termSize.lines < 20:
                Information("TERMINAL SIZE", "Terminal must be biger than 80 column and 20 lines.", style=STYLERROR)
                termSize = os.get_terminal_size()
        else:
            Information("TERMINAL SIZE", "Terminal must be biger than 80 column and 20 lines.", style=STYLSUCCESS)
        var = False
        while not var:
            value = Question3Value("GAME", "Would you join or create a new game", "join", "create", "Exit")
            if value == 1:
                var = self.joinGame()
            elif value == 0:
                var = self.createNewGame()
            else:
                doexit(0, "User exit")

    def joinGame(self):
        return self.getGameUrl()

    def getGameUrl(self):
        value = inputText("JOIN GAME", "Type game url")
        while value != None and not value.startswith("https://"):
            value = inputText("JOIN GAME", "Url must start with https://.", style=STYLERROR)
        if value == None:
            return False
        else:
            return True


    def createNewGame(self):
        dict = {}
        dict["ballwidth"] = self.getIntSettingRange("NEW GAME", "Ball width (5 - 30) :", 5, 30, 10)
        if dict["ballwidth"] == None:
            return False
        dict["planksize"] = self.getIntSettingRange("NEW GAME", "Plank size (10 - 40) :", 10, 40, 20)
        if dict["planksize"] == None:
            return False
        dict["speed"] = self.getFloatSettingRange("NEW GAME", "Speed (0.5 - 3) :", 0.5, 3, 1)
        if dict["speed"] == None:
            return False
        dict["acceleration"] = self.getIntSettingRange("NEW GAME", "Acceleration (0 - 10) :", 0, 10, 0)
        if dict["acceleration"] == None:
            return False
        dict["winpoint"] = self.getIntSettingRange("NEW GAME", "Win point (3 - 15) :", 3, 15, 5)
        if dict["winpoint"] == None:
            return False
        return True
        # dict["gamemode"] = self.getGameMode()


    def getIntSettingRange(self, title, text, min, max, default):
        value = inputText(title, text, False, STYLE, str(default))
        if value == None:
            return None
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
        if value == None:
            return None
        while value and (not match(floatPattern, value) or float(value) < min or float(value) > max):
            if not match(floatPattern, value):
                value = inputText(title, "Not a real number :", False, STYLERROR, str(default))
            else:
                value = inputText(title, ("Input must be between", min, "and", max, ":"), False, STYLERROR, str(default))
        return float(value)

