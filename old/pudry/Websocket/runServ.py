import asyncio
from wss_serv import WebSocketServer

async def main():
    ws = WebSocketServer("0.0.0.0", 8200)
    ws.run()
    while True:
        await asyncio.sleep(0.02)
        msg = ws.get_last_message()
        if msg:
            print("<=====================================>")
            for message in msg:
                print("Message :", message)

if __name__ == "__main__":
    asyncio.run(main())
