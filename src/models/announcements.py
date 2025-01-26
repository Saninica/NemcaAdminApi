from sqlalchemy import Column, Integer, ForeignKey, String, Text,DateTime
from sqlalchemy.sql import func
from sqlalchemy.orm import relationship
from src.database.base_class import Base


class Announcement(Base):
    __tablename__ = "announcements"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=True)
    body = Column(Text, nullable=True)
    cover_image = Column(String(255), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    start_date = Column(DateTime(timezone=True), nullable=True)
    end_date = Column(DateTime(timezone=True), nullable=True)

    page_id = Column(Integer, ForeignKey("pages.id", ondelete="CASCADE"), nullable=False, index=True)
    website_id = Column(Integer, ForeignKey("websites.id", ondelete="CASCADE"), nullable=False, index=True)
    language_id = Column(Integer, ForeignKey("languages.id", ondelete="CASCADE"), nullable=False, index=True)

    page = relationship("Page")
    website = relationship("Website")
    language = relationship("Language")

    def __repr__(self):
        return f"<Announcement id={self.id}-) title={self.title}>"