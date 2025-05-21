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

# TODO: temporarily use inmemory storage
@app.on_event("startup")
def startup_event():
    print("Startup event called")
    try:
        ingest_data()
    except Exception as e:
        print(f"ingest_data failed: {e}")
        raise


app.include_router(assistant.router)

@app.get("/")
def read_root():
    return {"message": "Hello, FastAPI!"}
