import asyncio
import websockets
import json
import aiosqlite
from alive_progress import alive_bar


async def initialize_db():
    print('started db...')
    conn = await get_db_connection()
    await conn.execute('''
        CREATE TABLE IF NOT EXISTS markets (
            type TEXT,
            id TEXT,
            name TEXT UNIQUE,
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
    await conn.commit()


async def get_db_connection():
    return await aiosqlite.connect('market.db')

async def store_data(data):
    markets = data.get('result', {}).get('data', {}).get('data', {})
    for market in markets:
        marketvals = await split_res(market)
        await insert_data(marketvals)

async def split_res(date):
    return date.split('|')


async def fetch_data(value='*', condition=''):
    conn = await get_db_connection()
    try:
        cursor = await conn.execute(f'SELECT * FROM markets')
        rows = await cursor.fetchall()
        return rows
    except Exception as e:
        print('-----------',e)
    finally:
        await conn.close()


async def insert_data(marketvals):
    conn = await get_db_connection()
    try:
        await conn.execute('INSERT INTO markets (type,id,name,sub_name,local_name,local_name_trans,value,high,low,close,change,change_percent,tolerance,time,datetime) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT (name) DO UPDATE SET value = EXCLUDED.value,high = EXCLUDED.high,low= EXCLUDED.low,close= EXCLUDED.close,change= EXCLUDED.change,change_percent= EXCLUDED.change_percent,tolerance = EXCLUDED.tolerance,time = EXCLUDED.time,datetime= EXCLUDED.datetime', (*marketvals,))
        await conn.commit()
    finally:
        await conn.close()
