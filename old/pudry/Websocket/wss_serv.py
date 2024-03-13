import websockets
import asyncio
class WebSocketServer:
    def __init__(self, host, port):
        self.host = host
        self.port = port
        self.clients = set()
        self.msg = []
        self.server_task = None
        self.player = [(0, ""), (0, ""), (0, ""), (0, "")]
        self.clientId = []
    
    def addClientId(self, src):
        clientId = id(src)
        if clientId not in self.clientId:
            self.clientId.append(clientId)
            for p in self.player:
                if not p[0]:
                    p[0] = id
                    p[1] = src[0]
                    break
        

    async def handle_client(self, websocket, path):
        # Ajoute le client à la liste des clients connectés
        id = 0
        self.clients.add(websocket)
        id = id(websocket)
        self.addClientId(websocket)
        try:
            async for message in websocket:
                print(id(message))
                # Stocke le message reçu dans la liste des messages
                self.msg.append(message)
                # Diffuse le message à tous les clients connectés, y compris l'expéditeur
                for client in self.clients:
                    await client.send(message)
        finally:
            print(f"Client {id} disconnected")
            if id:
                self.clientId.remove(id)
            self.clients.remove(websocket)


    async def start_server(self):
        # Démarrer le serveur WebSocket
        async with websockets.serve(self.handle_client, self.host, self.port):
            print(f"Serveur WebSocket démarré sur {self.host}:{self.port}...")
            # Laisser le serveur tourner indéfiniment
            await asyncio.Future()

    def run(self):
        # Démarrer le serveur WebSocket dans une tâche asynchrone
        self.server_task = asyncio.create_task(self.start_server())

    async def stop(self):
        # Arrêter le serveur WebSocket
        if self.server_task:
            self.server_task.cancel()
            await self.server_task

    def get_last_message(self):
        send = self.msg
        self.msg = []
        return send
