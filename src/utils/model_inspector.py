from sqlalchemy.inspection import inspect
from typing import Dict, List, Type
from src.database.base_class import Base
from src.utils.type_mapper import map_type  # Ensure this points to your type mapper
from src.schemas.model_metadata import FieldMetadata, ForeignKeyInfo


def get_models_metadata(models: List[Type[Base]]) -> Dict[str, Dict[str, FieldMetadata]]:
    metadata = {}
    for model in models:
        model_name = model.__name__
        if model_name == "Base":
            continue
        try:
            mapper = inspect(model)
            fields = {}
            for column in mapper.columns:
                field_info = {
                    "type": map_type(column.type),
                    "nullable": column.nullable,
                    "primary_key": column.primary_key,
                }
                
                # Check for ForeignKey
                foreign_keys = list(column.foreign_keys)
                if foreign_keys:
                    fk = foreign_keys[0]
                    target_table = fk.column.table.name
                    target_model = fk.column.table.name.capitalize()  # Adjust if necessary
                    target_field = fk.column.name
                    field_info["foreign_key"] = {
                        "target_table": target_table,
                        "target_model": target_model,
                        "target_field": target_field,
                    }
                
                
                fields[column.key] = FieldMetadata(**field_info)

            try: del fields["id"]
            except: pass

            try: del fields["created_at"]
            except: pass

            metadata[model_name] = fields
        except Exception as e:
            print(f"Error inspecting model {model_name}: {e}")
            raise e
    return metadata
