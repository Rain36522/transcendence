import asyncio
import pynput
import websockets
import ssl

def transmit_keys():
    # Start a keyboard listener that transmits keypresses into an
    # asyncio queue, and immediately return the queue to the caller.
    queue = asyncio.Queue()
    loop = asyncio.get_event_loop()
    def on_press(key):
        # this callback is invoked from another thread, so we can't
        # just queue.put_nowait(key.char), we have to go through
        # call_soon_threadsafe
        loop.call_soon_threadsafe(queue.put_nowait, key.char)
    def on_relase(key):
        # this callback is invoked from another thread, so we can't
        # just queue.put_nowait(key.char), we have to go through
            # call_soon_threadsafe
        print("Key relase")
        loop.call_soon_threadsafe(queue.put_nowait, str(key.char) + " off")
    pynput.keyboard.Listener(on_press=on_press, on_release=on_relase).start()
    return queue

async def main():
    ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
    ssl_context.check_hostname = False
    ssl_context.verify_mode = ssl.CERT_NONE
    key_queue = transmit_keys()
    async with websockets.connect("wss://127.0.0.1/wsGame/1/a", ssl=ssl_context) as websocket:
        while True:
            key = await key_queue.get()
            print("Pressed key :", str(key))

asyncio.run(main())