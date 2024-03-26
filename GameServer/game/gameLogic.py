from wsClient import WebSocketClient
import asyncio

class gameLogic:
    def __init__(self, client, gameSet, game):
        self.client = client
        self.game = game
        self.gameSet = gameSet
        print("data :", gameSet["user1"])

    """Client to game serv
    char 0 = player number
    char 1 : u = up, d = down
    """
    def getMsgs(self):
        messages = self.client.getMsg()
        msg = []
        if messages:
            user1 = str(self.gameSet.get("user1", ""))
            user2 = str(self.gameSet.get("user2", ""))
            user3 = str(self.gameSet.get("user3", ""))
            user4 = str(self.gameSet.get("user4", ""))
            for message in messages:
                if user1 and message.startswith(str(user1)):
                    message = message[len(user1):]
                    msg.append(message)
                elif user2 and message.startswith(user2):
                    message = message[len(user2):]
                    msg.append(message)
                elif user3 and message.startswith(user3):
                    message = message[len(user3):]
                    msg.append(message)
                elif user4 and message.startswith(user4):
                    message = message[len(user4):]
                    msg.append(message)
        return msg

    async def sendMsg(self):
        await self.client.sendMsg(self.game)

    async def gameInput(self):
        print("client message")
        self.game["ballx"] = 0
        self.game["bally"] = 0
        i = 0.013
        j = 0.025
        while True:
            messages = self.getMsgs()
            for msg in messages:
                print(msg)
                if msg[0] == "1":
                    self.game["p1"] = self.doCmd(self.game["p1"], msg[1])
                elif msg[0] == "2":
                    self.game["p2"] = self.doCmd(self.game["p2"], msg[1])
                elif msg[0] == "3":
                    self.game["p3"] = self.doCmd(self.game["p3"], msg[1])
                elif msg[0] == "4":
                    self.game["p4"] = self.doCmd(self.game["p4"], msg[1])
            
            self.game["ballx"] += i
            self.game["bally"] += j

            if self.game["ballx"] >= 0.5:
                i = -0.013
                self.game["ballx"] = 0.5
            elif self.game["ballx"] <= -0.5:
                i = 0.013
                self.game["ballx"] = -0.5
            if self.game["bally"] >= 0.5:
                j = -0.025
                self.game["bally"] = 0.5
            elif self.game["bally"] <= -0.5:
                j = 0.025
                self.game["bally"] = -0.5
            await self.sendMsg()
            await asyncio.sleep(0.05)
                    
            
    
    def doCmd(self, p, data):
        if data == "u":
            p += 0.025
        elif data == "d":
            p -= 0.025
        return p
