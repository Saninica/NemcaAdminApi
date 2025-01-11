from fastapi import APIRouter
from src.routes import user
from src.routes import pages
from src.routes import languages
from src.routes import contents
from src.routes import metadata
from src.routes import website
from src.routes import announcement
from src.routes import metatags
from src.dependencies import get_current_user
from fastapi import Depends


api_router = APIRouter()


api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(pages.router, prefix="/page", tags=["page"], dependencies=[Depends(get_current_user)])
api_router.include_router(languages.router, prefix="/language", tags=["language"],  dependencies=[Depends(get_current_user)])
api_router.include_router(contents.router, prefix="/content", tags=["content"],  dependencies=[Depends(get_current_user)])
api_router.include_router(metadata.router, prefix="/metadata", tags=["metadata"],  dependencies=[Depends(get_current_user)])
api_router.include_router(website.router, prefix="/website", tags=["website"],  dependencies=[Depends(get_current_user)])
api_router.include_router(announcement.router, prefix="/announcement", tags=["announcement"],  dependencies=[Depends(get_current_user)])
api_router.include_router(metatags.router, prefix="/metatag", tags=["metatag"],  dependencies=[Depends(get_current_user)])