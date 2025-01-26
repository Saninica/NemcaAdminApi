from .base import CRUDBase
from src.models.website import Website
from src.schemas.website import WebsiteCreate, WebsiteUpdate
from fastapi import UploadFile
from src.models.pages import Page, PageContent
from src.models.announcements import Announcement
from src.models.metatags import MetaTag
from src.models.blogs import Blog
from src.models.languages import Language
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession


class CRUDWebsite(CRUDBase[Website, WebsiteCreate, WebsiteUpdate]):
    async def upload_favicon(self, favicon: UploadFile):
        favicon_path = f"media/website/{favicon.filename}"

        with open(favicon_path, "wb+") as f:
            f.write(await favicon.read())

        return favicon_path

    async def get_all_website_info(self, db: AsyncSession, website_id: int, language_code: str):
        # Filter data from the database
        pages = (await db.execute(select(Page).where(Page.website_id == website_id))).scalars().all()
        languages = (await db.execute(
            select(Language).where(Language.website_id == website_id)
        )).scalars().first()

        page_contents = (await db.execute(
            select(PageContent).where(
                PageContent.website_id == website_id,
                PageContent.language_id == languages.id
            )
        )).scalars().all()
        announcements = (await db.execute(
            select(Announcement).where(
                Announcement.website_id == website_id,
                Announcement.language_id == languages.id
            )
        )).scalars().all()
        metatags = (await db.execute(
            select(MetaTag).where(
                MetaTag.website_id == website_id,
                MetaTag.language_id == languages.id
            )
        )).scalars().all()
        blogs = (await db.execute(
            select(Blog).where(
                Blog.website_id == website_id,
                Blog.language_id == languages.id
            )
        )).scalars().all()
        languages = (await db.execute(
            select(Language).where(Language.website_id == website_id)
        )).scalars().all()
        websites = (await db.execute(
            select(Website).where(Website.id == website_id)
        )).scalars().all()

        # Construct the response
        return {
        "page": [
            {"id": page.id, "name": page.name, "website_id": page.website_id}
            for page in pages
        ],
        "contents": [
            {
                "id": content.id,
                "page": content.page.name,
                "website": content.website.name,
                "title": content.title,
                "body": content.body,
                "cover_image": content.cover_image
            }
            for content in page_contents
        ],
        "languages": [
            {"code": lang.code, "name": lang.name}  # or add website_id if you like
            for lang in languages
        ],
        "websites": [
            {
                "id": w.id,
                "name": w.name,
                "domain_url": w.domain_url,
                "favicon_image": w.favicon_image,
            }
            for w in websites
        ],
        "announcements": [
            {
                "id": a.id,
                "title": a.title,
                "body": a.body,
                "cover_image": a.cover_image,
                "start_date": a.start_date.isoformat() if a.start_date else None,
                "end_date": a.end_date.isoformat() if a.end_date else None,
                "created_at": a.created_at.isoformat() if a.created_at else None,
                "page_id": a.page_id,
                "website_id": a.website_id,
            }
            for a in announcements
        ],
        "metatags": [
            {
                "id": m.id,
                "title": m.title,
                "description": m.description,
                "keywords": m.keywords,
                "page_id": m.page_id,
                "website_id": m.website_id,
            }
            for m in metatags
        ],
        "blogs": [
            {
                "id": b.id,
                "website_id": b.website_id,
                "page_id": b.page_id,
                "body": b.body
            }
            for b in blogs
        ],
    }

crud_website = CRUDWebsite(Website)
