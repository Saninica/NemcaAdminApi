from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from src.database.base_class import Base


class Page(Base):
    __tablename__ = "pages"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(50), unique=True, nullable=False)  # e.g., 'home', 'about_us'

    def __repr__(self):
        return f"<Page(id={self.id}, name='{self.name}')>"


class PageContent(Base):
    __tablename__ = "page_contents"

    id = Column(Integer, primary_key=True)
    page_id = Column(Integer, ForeignKey("pages.id", ondelete="CASCADE"), nullable=False, index=True)
    language_code = Column(String(2), ForeignKey("languages.code", ondelete="CASCADE"), nullable=False, index=True)
    title = Column(String(100), nullable=False)
    body = Column(Text, nullable=False)
    page = relationship("Page")
    language = relationship("Language")

    def __repr__(self):
        return f"<PageContent(id={self.id}, page_id={self.page_id}>"