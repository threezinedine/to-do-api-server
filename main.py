import os
from fastapi import FastAPI
from dotenv import load_dotenv


app = FastAPI()


if __name__ == "__main__":
    import uvicorn
    load_dotenv()
    host = os.getenv("API_HOST", "127.0.0.1")
    port = int(os.getenv("API_PORT", 8000))

    uvicorn.run("main:app", host=host, port=port, reload=True)
