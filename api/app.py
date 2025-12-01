from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import os
import asyncpg
from contextlib import asynccontextmanager

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

async def get_db_connection():
    return await asyncpg.connect(
        host=os.getenv('DB_HOST', 'db'),
        port=os.getenv('DB_PORT', 5432),
        user=os.getenv('DB_USER', 'postgres'),
        password=os.getenv('DB_PASSWORD', 'password'),
        database=os.getenv('DB_NAME', 'appdb')
    )

@app.get("/status")
async def status():
    return {"status": "OK"}

@app.get("/items")
async def get_items():
    conn = await get_db_connection()
    try:
        rows = await conn.fetch('SELECT * FROM items')
        return [dict(row) for row in rows]
    finally:
        await conn.close()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
