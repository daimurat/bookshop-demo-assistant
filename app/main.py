import os
import weave
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import assistant
from ingest import ingest_data

# TODO: temporarily use inmemory storage
@asynccontextmanager
async def lifespan(app: FastAPI):
    try:
        ingest_data()
    except Exception as e:
        print(f"ingest_data failed: {e}")
        raise
    yield

app = FastAPI(lifespan=lifespan)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

weave.init(os.environ.get("WEAVE_PROJECT"))

app.include_router(assistant.router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
