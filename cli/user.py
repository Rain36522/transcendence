from color import *
from os import get_terminal_size, system


def separator(begin, middle, end):
    y, x = get_terminal_size()
    print(begin, end="")
    while y > len(begin) + len(end):
        print("=", end="")
        y -= 2
    print(end)

class userCli:
    def __init__(self):
        self.username = ""
        self.userToken = None
        self.cookie = None
        while not self.chooseMethode():
            pass
        

    def chooseMethode(self):
        system("clear")
        choice = ""
        while choice != "1" or choice != "2":
            print(BWHITE, "1 :", WHITE, "Would you like to login?", RESET)
            print(BWHITE, "2 :", WHITE, "Would you like to create a account?", RESET)
            choice = input("1 - 2 : ")
            if choice != "1" or choice != "2":
                print(ORANGE, "Wrong input!", RESET)
        system("clear")
        if choice == "1":
            return self.getLoginInfo()
        elif choice == "2":
            return self.getNewUserData()

    def getLoginInfo(self):
        print(BWHITE, "Login", RESET)
        username = input("User : ")
        pwd = input("password : ")
        self.doLogin(username, pwd)
    
    def doLogin(self, username: str, pwd: str):
        #django login process
        loged = False
        self.username = username
        if not loged:
            loged = True # TODO Remove this line
            print(ORANGE, "Wrong login information!", RESET)
            self.loginattempts += 1
            self.getLoginInfo()
        else:
            print(GREEN, "Login success.", RESET)
            self.loginattempts = 0


    def getNewUserData(self):
        print(BBLUE, "New user creation", RESET)
        username = input("User : ")
        mail = input("mail : ")
        pwd1 = input("password : ")
        pwd2 = input("password check : ")
        while pwd1 != pwd2:
            print(RED, "Different password. Try again", RESET)
            pwd1 = input("password : ")
            pwd2 = input("password check : ")
        separator("<", "=", ">")
        print("username : ", username)
        print("mail : ", mail)
        value = input("Did you put the right information? [yes/no/exit]")
        if value == "y" or value == "yes":
            self.createNewUser()        
        elif value == "e" or value == "no":
            return False
        else:
            self.chooseMethode()
        return True
    
    def createNewUser(self, user, mail, pwd):
        self.username = user
    
        