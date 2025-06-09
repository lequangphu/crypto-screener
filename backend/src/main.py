from fastapi import FastAPI
from api.routes import router
import uvicorn

app = FastAPI()

app.include_router(router)

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Crypto Screener Backend!"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000) 