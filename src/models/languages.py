from sqlalchemy import Column, Integer, ForeignKey, String, Text
from sqlalchemy.orm import relationship
from src.database.base_class import Base


class Language(Base):
    __tablename__ = "languages"

    code = Column(String(2), primary_key=True, index=True)  # e.g., 'en', 'tr'
    name = Column(String(50), unique=True, nullable=False)  # e.g., 'English', 'Turkish'
    website_id = Column(Integer, ForeignKey("websites.id", ondelete="CASCADE"), nullable=False, index=True)
    website = relationship("Website")
