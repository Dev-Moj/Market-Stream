from fastapi import FastAPI
import aiosqlite
from pydantic import BaseModel

app = FastAPI()



@app.get("/")
async def read_preferences(name=None):

    async with aiosqlite.connect('market.db') as db:
        cursor = await db.execute(f'SELECT value FROM markets WHERE name = price_dollar_rl;')
        rows = await cursor.fetchall()
        preferences = [{row[0]:row} for row in rows]
        return preferences


import uvicorn
uvicorn.run(app, host="0.0.0.0", port=8002)
