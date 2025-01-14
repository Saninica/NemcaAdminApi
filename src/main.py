from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.routes import api_router
from src.core.config import settings
from fastapi.staticfiles import StaticFiles
from pathlib import Path


app = FastAPI(title="Nemca Admin API", version="1.0.0")

media_dir =  Path = Path(__file__).resolve().parent.parent / "media"
media_url = f"/media"

app.mount(media_url, StaticFiles(directory=media_dir), name="media")


app.include_router(prefix="/api", router=api_router)


app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:5173",
        "http://localhost:5174",
        "http://localhost:3000",
        settings.SERVER_IP

    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)


