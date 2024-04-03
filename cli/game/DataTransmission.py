from prompt_toolkit import prompt
from prompt_toolkit.key_binding import KeyBindings
import asyncio
from json import loads

class DataTransmission:
    def __init__(self, url):
        self.message = None
        self.wsCli = None
        self.url = url

    
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



class KeyBinding:
    def __init__(self, username, usertoken, KeyUp, KeyDown, wsCli):
        self.usertoken = usertoken
        self.username = username
        self.wsCli = wsCli
        self.kb = KeyBindings()
        self.kb.add(keyUp)(self.keyUp)  # Supprimer les parenthèses ici
        self.kb.add(KeyDown)(self.keyDown)  # Supprimer les parenthèses ici

    async def KeyUp(self, event):
        await self.wsCli.send(self.usertoken + "u")
    
    async def KeyDown(self, event):
        await self.wsCli.send(self.usertoken + "u")

    async def loop():
        while True:
            user_input = await prompt('', key_bindings=self.kb)
            await asyncio.sleep(0.01)
        
