from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import api_router

app = FastAPI(title="Nemca Admin API", version="1.0.0")


app.include_router(api_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


