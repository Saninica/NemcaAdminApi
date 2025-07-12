from sqlalchemy import Column, Integer, ForeignKey, String, Text, Float
from sqlalchemy.orm import relationship
from src.database.base_class import Base
from sqlalchemy.types import JSON


class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), nullable=False)  # e.g., 'home', 'about_us'
    website_id = Column(Integer, ForeignKey("websites.id", ondelete="CASCADE"), nullable=False, index=True)
    website = relationship("Website")

    def __repr__(self):
        return f"<Page(id={self.id}, name='{self.name}')>"


class PageContent(Base):
    __tablename__ = "page_contents"

    id = Column(Integer, primary_key=True)
    title = Column(String(100), nullable=False)
    body = Column(Text, nullable=False)
    price = Column(Float, nullable=True)
    cover_images = Column(JSON, nullable=True)
    page_id = Column(Integer, ForeignKey("pages.id", ondelete="CASCADE"), nullable=False, index=True)
    language_id = Column(Integer, ForeignKey("languages.id", ondelete="CASCADE"), nullable=False, index=True)
    website_id = Column(Integer, ForeignKey("websites.id", ondelete="CASCADE"), nullable=False, index=True)
    page = relationship("Page")
    language = relationship("Language")
    website = relationship("Website")


    def __repr__(self):
        return f"<PageContent(id={self.id}, page_id={self.page_id}>"