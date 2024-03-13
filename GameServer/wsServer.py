import websockets
import asyncio

class WebSocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = set()
    
    async def handle_client(self, websocket, path):
        self.clients.add(websocket)
        print("path :", path)
        print(websocket.remote_address[0])
        for client in self.clients:
            await client.send(websocket.remote_address[0])
        try:
            async for message in websocket:
                print(message)
                for client in self.clients:
                    await client.send(message)
        finally:
            self.clients.remove(websocket)

    async def start_server(self):
        print("Server is runing in : " + self.host + ":" + str(self.port))
        async with websockets.serve(self.handle_client, self.host, self.port):
            await asyncio.Future()

    def run(self):
        asyncio.create_task(self.start_server())



async def main():
    ws = WebSocketServer("0.0.0.0", 8001)
    ws.run()
    while True:
        await asyncio.sleep(0.02)

if __name__ == "__main__":
    asyncio.run(main())
