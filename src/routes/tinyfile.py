from fastapi import APIRouter, UploadFile, File
from urllib.parse import quote
from src.core.config import settings


router = APIRouter()

@router.post("/")
async def tinyfile(file: UploadFile = File(None)):
    file_path = f"media/tinyfile/{file.filename}"

    with open(file_path, "wb+") as f:
        f.write(await file.read())

    url_path = f"http://127.0.0.1:8000{settings.ROOT_PATH}/media/tinyfile/{quote(file.filename)}"

    return {"location": url_path}
