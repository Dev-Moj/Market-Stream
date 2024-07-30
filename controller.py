import asyncio
import websockets
import json
import aiosqlite
from alive_progress import alive_bar
from fastapi import FastAPI

app = FastAPI()

async def initialize_db():
    print('started db...')
    async with aiosqlite.connect('market.db') as db:
        await db.execute('''
            CREATE TABLE IF NOT EXISTS markets (
                type TEXT,
                id TEXT,
                name TEXT,
                sub_name TEXT,
                local_name TEXT,
                local_name_trans TEXT,
                value TEXT,
                high TEXT,
                low TEXT,
                close TEXT,
                change TEXT,
                change_percent TEXT,
                tolerance TEXT,
                time TEXT,
                datetime TEXT
            )
        ''')
        await db.commit()

async def store_data(data):
    async with aiosqlite.connect('market.db') as db:
        await db.execute('INSERT INTO markets (type,id,name,sub_name,local_name,local_name_trans,value,high,low,close,change,change_percent,tolerance,time,datetime) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', (*data,))
        await db.commit()

async def split_res(date):
    data = date.split('|')
    await store_data(data)


async def read_res(date):
    markets = date.get('result', {}).get('data', {}).get('data', {})
    for i in markets:
        await split_res(i)

async def connect_to_websocket(uri):
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
                                await read_res(data)
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


async def main():
    await initialize_db()
    await connect_to_websocket('wss://stream.tgju.org/connection/websocket')



if __name__ == "__main__":
    asyncio.run(main())
