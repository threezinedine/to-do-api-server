import os
from fastapi import FastAPI
from dotenv import load_dotenv

from app.api.v1 import users


app = FastAPI()
app.include_router(users.router)


if __name__ == "__main__":
    import uvicorn
    load_dotenv()
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", 8000))

    uvicorn.run("main:app", host=host, port=port, reload=True)
