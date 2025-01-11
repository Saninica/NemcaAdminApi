from .base import CRUDBase
from src.models.metatags import MetaTag
from src.schemas.metatags import MetatagsCreate, MetatagsUpdate


class CrudMetatags(CRUDBase[MetaTag, MetatagsCreate, MetatagsUpdate]):
    pass

crud_metatags = CrudMetatags(MetaTag)