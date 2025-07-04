from fastapi import FastAPI
from pydantic import BaseModel

@app.get("/")
async def root():
    return {"message": "alive"}
