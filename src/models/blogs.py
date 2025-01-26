from sqlalchemy import Column, Integer, String, Text,DateTime, ForeignKey
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.database.base_class import Base


class Blog(Base):
    __tablename__ = "blogs"

    id = Column(Integer, primary_key=True, index=True)
    body = Column(Text, index=True, nullable=True)
    website_id = Column(Integer, ForeignKey("websites.id", ondelete="CASCADE"), nullable=True, index=True)
    language_id = Column(Integer, ForeignKey("languages.id", ondelete="CASCADE"), nullable=True, index=True)
    page_id = Column(Integer, ForeignKey("pages.id", ondelete="CASCADE"), nullable=True, index=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    page = relationship("Page")
    language = relationship("Language")
    website = relationship("Website")

    def __repr__(self) -> str:
        return f"Blog(id={self.id}, website_id={self.website_id}, language_code={self.language_code})"