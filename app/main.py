from fastapi import FastAPI
from app.routers import assistant
from ingest import ingest_data

ingest_data()

app = FastAPI()

app.include_router(assistant.router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
