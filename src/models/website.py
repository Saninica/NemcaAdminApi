from sqlalchemy import Column, Integer, String
from src.database.base_class import Base


class Website(Base):
    __tablename__ = "websites"

    id = Column(Integer, primary_key=True)
    name = Column(String(255), nullable=False)
    domain_url = Column(String(255), nullable=False)
    favicon_image = Column(String(255), nullable=True)
    
    
    def __repr__(self):
        return f"<Website( name='{self.name}')"