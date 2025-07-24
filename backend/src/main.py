from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from routes import router as api_router

app = FastAPI(title="AI-powered Insights Cloud", version="1.0.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

app.include_router(api_router, prefix="/api")


@app.get("/")
def root():
    return {
        "message": "Welcome to the File (AI-powered) Insights API. The best you will ever find"
    }
