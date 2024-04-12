import websockets
from pynput.keyboard import Listener, Key
import asyncio
from json import loads

class DataTransmission:
    def __init__(self, gameSettings, url):
        self.gameSettings = gameSettings
        self.message = None
        self.wsCli = None
        self.url = url + "/game/" + int(gameSettings["gameId"])
        self.w = False
        self.s = False
        self.u = False
        self.d = False
        self.is2player = gameSettings["isSolo"] and gameSettings["nbPlayers"] == 2
        if gameSettings["isSolo"]:
            self.playerpos = 1
        else:
            self.playerpos = 0


    
    async def ConnectWs(self):
        while not self.wsCli:
            try:
                self.wsCli = await websockets.connect(self.url)
                print("ws Server successfully connected to :", self.url)
            except Exception as e:
                print("ws Server connection failed")
                self.wsCli = None
                await asyncio.sleep(0.5)
    
    async def receive_messages(self):
        try:
            async for self.message in self.websocket:
                if not self.playerpos:
                    self.getUserPos()
        except:
            await self.ConnectWs()
    
    def getUserPos(self):
        if self.message["users"][0] == self.gameSettings["user"]:
            self.playerpos = 1
        else:
            self.playerpos = 2

    def getMessage(self):
        return loads(self.message)
    
    async def disconnect(self):
        await self.wsCli.close()

    def on_press(self, key):
        if len(str(key)) == 3:
            print("\b ", end="")
        elif len(str(key)) == 6 or len(str(key)) == 8:
            print("\b\b\b\b    ", end="")
        if len(str(key)) == 3 and key.char == "w" and not self.w:
            self.w = True
            self.wsCli.send(str(self.playerpos) + "u-on")
        elif len(str(key)) == 3 and key.char == "s" and not self.s:
            self.s = True
            self.wsCli.send(str(self.playerpos) + "d-on")
        elif len(str(key)) == 6 and key == Key.up and not self.u and self.is2player:
            self.u = True
            self.wsCli.send("2u-on")
        elif len(str(key)) == 8 and key == Key.down and not self.d and self.is2player:
            self.d = True
            self.wsCli.send("2d-on")

    def on_release(self, key):
        if len(str(key)) == 3: # replace char by space
            print("\b ", end="")
        elif len(str(key)) == 6 or len(str(key)) == 8:
            print("\b\b\b\b    ", end="")
        if len(str(key)) == 3 and key.char == "w" and self.w:
            self.w = False
            self.wsCli.send(str(self.playerpos) + "u-off")
        elif len(str(key)) == 3 and key.char == "s" and self.s:
            self.s = False
            self.wsCli.send(str(self.playerpos) + "d-off")
        elif len(str(key)) == 6 and key == Key.up and self.u and self.is2player:
            self.wsCli.send("2u-off")
            self.u = False
        elif len(str(key)) == 8 and key == Key.down and self.d and self.is2player:
            self.d = False
            self.wsCli.send("2d-off")
        
    def run(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()


# game = {
# 	"ballx" : 0, # -0.5 -> 0.5
# 	"bally" : 0, # -0.5 -> 0.5
# 	"p1" : 0, # -0.5 -> 0.5
# 	"p2" : 0, # -0.5 -> 0.5
# 	"p3" : 0, # -0.5 -> 0.5
# 	"p4" : 0, # -0.5 -> 0.5
# 	"state" : "playing",
# 	"score1" : 0,
# 	"score2" : 0,
# 	"score3" : 0,
# 	"score4" : 0,
#   "users" : ["usera", "userb"]
# }


# class KeyBinding:
#     def __init__(self, username, usertoken, KeyUp, KeyDown, wsCli):
#         self.usertoken = usertoken
#         self.username = username
#         self.wsCli = wsCli
#         self.kb = KeyBindings()
#         self.kb.add(keyUp)(self.keyUp)  # Supprimer les parenthèses ici
#         self.kb.add(KeyDown)(self.keyDown)  # Supprimer les parenthèses ici

#     async def KeyUp(self, event):
#         await self.wsCli.send(self.usertoken + "u")
    
#     async def KeyDown(self, event):
#         await self.wsCli.send(self.usertoken + "u")

#     async def loop():
#         while True:
#             user_input = await prompt('', key_bindings=self.kb)
#             await asyncio.sleep(0.01)
        
