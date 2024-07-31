import asyncio
import websockets
import json
import aiosqlite
from alive_progress import alive_bar
from app.database.db_operations import store_data



async def collect_data(uri):
    print(uri)
    print('Started Connection...')
    while True:
        try:
            async with websockets.connect(uri) as websocket:
                print("Connected to WebSocket.")
                await websocket.send(json.dumps({"params":{"name":"js"},"id":1}))
                await websocket.send(json.dumps({"method":1,"params":{"channel":"tgju:stream"},"id":2}))
                with alive_bar() as bar:
                    while True:
                        response = await websocket.recv()
                        if response:

                            try:
                                data = json.loads(response)
                                await store_data(data)
                                bar()
                            except Exception as e:
                                pass

        except websockets.ConnectionClosedError:
            print("Connection closed. Attempting to reconnect...")
            with alive_bar(5, title='Reconnecting in') as bar:
                for _ in range(5):
                    await asyncio.sleep(1)
                    bar()
        except Exception as e:
            print(f"An error occurred: {e}")
            with alive_bar(5, title='Retrying in') as bar:
                for _ in range(5):
                    await asyncio.sleep(1)
                    bar()



if __name__ == "__main__":
    uri = "ws://example.com/socket"
    asyncio.run(collect_data(uri))
