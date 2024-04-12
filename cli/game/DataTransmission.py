from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
import asyncio
from json import loads

class DataTransmission:
    def __init__(self, url):
        self.message = None
        self.wsCli = None
        self.url = url
        self.w = False
        self.s = False
        self.u = False
        self.d = False
        self.is2player = True

    
    async def ConnectWs(self):
        while not self.wsCli:
            try:
                ws.Cli = await websockets.connect(self.url)
                print("ws Server successfully connected to :", self.url)
            except Exception as e:
                print("ws Server connection failed")
                self.wsCli = None
                await asyncio.sleep(0.5)
    
    async def receive_messages(self):
        try:
            async for self.message in self.websocket:
                pass
        except:
            await self.ConnectWs()  
    
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
        elif len(str(key)) == 3 and key.char == "s" and not self.s:
            self.s = True
        elif len(str(key)) == 6 and key == Key.up and not self.u and self.is2player:
            self.u = True
        elif len(str(key)) == 8 and key == Key.down and not self.d and self.is2player:
            self.d = True

    def on_release(self, key):
        if len(str(key)) == 3: # replace char by space
            print("\b ", end="")
        elif len(str(key)) == 6 or len(str(key)) == 8:
            print("\b\b\b\b    ", end="")
        if len(str(key)) == 3 and key.char == "w" and self.w:
            self.w = False
        elif len(str(key)) == 3 and key.char == "s" and self.s:
            self.s = False
        elif len(str(key)) == 6 and key == Key.up and self.u and self.is2player:
            self.u = False
        elif len(str(key)) == 8 and key == Key.down and self.d and self.is2player:
            self.d = False
        
    def run(self):
        with Listener(on_press=self.on_press, on_release=self.on_release) as listener:
            listener.join()




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
        
