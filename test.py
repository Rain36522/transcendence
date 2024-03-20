import asyncio
import websockets

async def test_websocket_connection():
    uri = "ws://localhost:8000/ws/chat/"
    async with websockets.connect(uri) as websocket:
        # Send a test message
        await websocket.send("Hello, WebSocket!")
        print("Message sent.")
        
        # Receive and print the response
        response = await websocket.recv()
        print("Response received:", response)

# Run the test function
asyncio.get_event_loop().run_until_complete(test_websocket_connection())