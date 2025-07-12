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
                # Get enhanced type mapping with constraints
                type_info = map_type(column.type)
                
                field_info = {
                    "input_type": type_info["input_type"],
                    "nullable": column.nullable,
                    "primary_key": column.primary_key,
                    "constraints": type_info["constraints"],
                }
                
                # Add additional constraints from column attributes
                if hasattr(column, 'default') and column.default is not None:
                    field_info["constraints"]["default"] = str(column.default.arg) if hasattr(column.default, 'arg') else str(column.default)
                
                if hasattr(column, 'unique') and column.unique:
                    field_info["constraints"]["unique"] = True
                
                if hasattr(column, 'index') and column.index:
                    field_info["constraints"]["indexed"] = True
                
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
                    # Override input type for foreign keys
                    field_info["input_type"] = "select"
                
                fields[column.key] = FieldMetadata(**field_info)

            try: del fields["id"]
            except: pass

            try: del fields["created_at"]
            except: pass

            try: del fields["user_id"]
            except: pass

            metadata[model_name] = fields
        except Exception as e:
            print(f"Error inspecting model {model_name}: {e}")
            raise e
    return metadata
