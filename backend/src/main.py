from fastapi import FastAPI
from .api.routes import router

app = FastAPI()

app.include_router(router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Crypto Screener Backend!"} 