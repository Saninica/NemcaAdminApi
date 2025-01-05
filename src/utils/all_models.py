import pkgutil
import importlib
from sqlalchemy.ext.declarative import DeclarativeMeta
from typing import List
from src.database.base_class import Base

def get_all_sqlalchemy_models() -> List[DeclarativeMeta]:
    models = []
    package = 'src.models' 
    package_module = importlib.import_module(package)


    for loader, module_name, is_pkg in pkgutil.iter_modules(package_module.__path__):
        module = importlib.import_module(f"{package}.{module_name}")
        for attr_name in dir(module):
            attr = getattr(module, attr_name)
            if isinstance(attr, DeclarativeMeta) and hasattr(attr, '__tablename__'):
                models.append(attr)
    return models