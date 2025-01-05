from fastapi import APIRouter
from src.routes import user
from src.routes import pages
from src.routes import languages
from src.routes import contents
from src.routes import metadata

api_router = APIRouter()
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(pages.router, prefix="/page", tags=["page"])
api_router.include_router(languages.router, prefix="/language", tags=["language"])
api_router.include_router(contents.router, prefix="/content", tags=["content"])
api_router.include_router(metadata.router, prefix="/metadata", tags=["metadata"])