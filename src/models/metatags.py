from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from src.database.base_class import Base


class MetaTag(Base):
    __tablename__ = "metatags"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    keywords = Column(Text, nullable=True)
    page_id = Column(Integer, ForeignKey("pages.id", ondelete="CASCADE"), nullable=False, index=True)
    language_code = Column(String(2), ForeignKey("languages.code", ondelete="CASCADE"), nullable=False, index=True)
    website_id = Column(Integer, ForeignKey("websites.id", ondelete="CASCADE"), nullable=False, index=True)
    website = relationship("Website")
    page = relationship("Page")
    language = relationship("Language")