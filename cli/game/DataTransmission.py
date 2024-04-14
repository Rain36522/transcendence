import websockets
from pynput.keyboard import Listener, Key
import pynput
import asyncio
from json import loads
from color import *
import ssl

class DataTransmission:
    def __init__(self, gameSettings, url):
        self.gameSettings = gameSettings
        self.message = None
        self.errormsg = 0
        self.wsCli = None
        self.url = "wss" + url[5:] + "/wsGame/" + str(gameSettings["gameid"]) + "/" + str(gameSettings["user"]) + "/"
        self.w = False
        self.s = False
        self.u = False
        self.d = False
        self.isConnected = False
        self.runKeyBinding = False
        self.is2player = gameSettings["isSolo"] and gameSettings["nbPlayers"] == 2
        if gameSettings["isSolo"]:
            self.playerpos = 1
        else:
            self.playerpos = 0


    
    async def ConnectWsKeyBinding(self):
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        ssl_context.check_hostname = False
        ssl_context.verify_mode = ssl.CERT_NONE
        
        while not self.wsCli:
            try:
                self.wsCli = await websockets.connect(self.url, ssl=ssl_context)
                self.isConnected = True
                while not self.runKeyBinding and not self.errormsg:
                    await asyncio.sleep(0.1)
                # if not self.errormsg:
                #     KeyQueue = self.transmitKeys()
                i = 0
                while not self.errormsg and self.runKeyBinding:
                    i += 1
                    if i == 1:
                        await self.wsCli.send("1u-on")
                    if i == 2:
                        await self.wsCli.send("1u-off")
                    await asyncio.sleep(0.1)
                    # key = await KeyQueue.get()
                    # if key == "EXIT":
                    #     return self.errormsg
                    # await self.wsCli.send(key)
                return self.errormsg
            except Exception as e:
                print("ws Server connection failesd,", self.url)
                self.wsCli = None
                self.isConnected = False

    async def receive_messages(self):
        while not self.wsCli:
            await asyncio.sleep(0.1)
        while True:
            # try:
            async for self.message in self.wsCli:
                if str(self.message).isdigit():
                    self.errormsg = self.message
                    return self.errormsg
                self.runKeyBinding = True
                if not self.playerpos:
                    self.getUserPos()
            # except:
            #     print(RED, "Reading msg error", RESET)
            #     while not self.isConnected:
            #         await asyncio.sleep(0.1)
    
    def getUserPos(self):
        msg = loads(self.message)
        if msg["users"][0] == self.gameSettings["user"]:
            self.playerpos = 1
        else:
            self.playerpos = 2

    def getMessage(self):
        if self.message:
            return loads(self.message)
        else:
            return None
    
    async def disconnect(self):
        await self.wsCli.close()
    
    def transmitKeys(self):
        queue = asyncio.Queue()
        loop = asyncio.get_event_loop()
        def on_press(key):
            if self.errormsg:
                loop.call_soon_threadsafe(queue.put_nowait, "EXIT")
                return
            if len(str(key)) == 3:
                print("\b ", end="")
            elif len(str(key)) == 6 or len(str(key)) == 8:
                print("\b\b\b\b    ", end="")
            if len(str(key)) == 3 and key.char == "w" and not self.w:
                self.w = True
                loop.call_soon_threadsafe(queue.put_nowait, str(self.playerpos) + "u-on")
            elif len(str(key)) == 3 and key.char == "s" and not self.s:
                self.s = True
                loop.call_soon_threadsafe(queue.put_nowait, str(self.playerpos) + "d-on")
            elif len(str(key)) == 6 and key == Key.up and not self.u and self.is2player:
                self.u = True
                loop.call_soon_threadsafe(queue.put_nowait, "2u-on")
            elif len(str(key)) == 8 and key == Key.down and not self.d and self.is2player:
                self.d = True
                loop.call_soon_threadsafe(queue.put_nowait, "2d-on")

        def on_release(key):
            if self.errormsg:
                loop.call_soon_threadsafe(queue.put_nowait, "EXIT")
                return
            if len(str(key)) == 3 and key.char == "w" and self.w:
                self.w = False
                loop.call_soon_threadsafe(queue.put_nowait, str(self.playerpos) + "u-off")
            elif len(str(key)) == 3 and key.char == "s" and self.s:
                self.s = False
                loop.call_soon_threadsafe(queue.put_nowait, str(self.playerpos) + "d-off")
            elif len(str(key)) == 6 and key == Key.up and self.u and self.is2player:
                self.u = False
                loop.call_soon_threadsafe(queue.put_nowait, "2d-on")
            elif len(str(key)) == 8 and key == Key.down and self.d and self.is2player:
                self.d = False
                loop.call_soon_threadsafe(queue.put_nowait, "2d-off")
        pynput.keyboard.Listener(on_press=on_press, on_release=on_release).start()
        return queue


    # async def runKeyBinding(self):
            # await websockets.send(key)


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
#         await await self.wsCli.send(self.usertoken + "u")
    
#     async def KeyDown(self, event):
#         await await self.wsCli.send(self.usertoken + "u")

#     async def loop():
#         while True:
#             user_input = await prompt('', key_bindings=self.kb)
#             await asyncio.sleep(0.01)