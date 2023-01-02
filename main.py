import os
from fastapi import FastAPI
from dotenv import load_dotenv

from app.api.v1 import users
from app.constants import (
    DEFAULT_HOST_KEY,
    DEFAULT_HOST,
    DEFAULT_PORT_KEY,
    DEFAULT_PORT,
)


app = FastAPI()
app.include_router(users.router)


if __name__ == "__main__":
    import uvicorn
    load_dotenv()
    host = os.getenv(DEFAULT_HOST_KEY, DEFAULT_HOST)
    port = int(os.getenv(DEFAULT_PORT_KEY, DEFAULT_PORT))

    uvicorn.run("main:app", host=host, port=port, reload=True)
