from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import assistant
from ingest import ingest_data

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(assistant.router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
