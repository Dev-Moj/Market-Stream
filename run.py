import asyncio
import uvicorn
from multiprocessing import Process
from app.websocket.collector import collect_data
from app.database.db_operations import initialize_db

def start_websocket_collector():
    uri = "wss://stream.tgju.org/connection/websocket"
    asyncio.run(collect_data(uri))

def start_fastapi():
    uvicorn.run("app.main:app", host="0.0.0.0", port=8000, reload=True)

if __name__ == "__main__":
    asyncio.run(initialize_db())
    p1 = Process(target=start_websocket_collector)
    p2 = Process(target=start_fastapi)
    p1.start()
    p2.start()
    p1.join()
    p2.join()
