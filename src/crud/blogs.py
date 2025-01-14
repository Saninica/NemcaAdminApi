from .base import CRUDBase
from src.models.blogs import Blog
from src.schemas.blogs import BlogCreate, BlogUpdate


class CRUDBlog(CRUDBase[Blog, BlogCreate, BlogUpdate]):
    pass

crud_blog = CRUDBlog(Blog)
