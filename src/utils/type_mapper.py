from sqlalchemy import (
    Integer, String, Boolean, DateTime, Float, Text, Date, Time, Numeric, LargeBinary, Enum, JSON
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.types import TypeEngine

# Define a mapping from SQLAlchemy types to Python type names
TYPE_MAPPING = {
    Integer: "int",
    String: "str",
    Boolean: "bool",
    DateTime: "datetime",
    Float: "float",
    Text: "str",
    Date: "date",
    Time: "time",
    Numeric: "float",
    LargeBinary: "bytes",
    Enum: "enum",
    JSON: "dict",
    ARRAY: "list",
    # Add more mappings as needed
}

def map_type(sqlalchemy_type: TypeEngine) -> str:
    for sa_type, py_type in TYPE_MAPPING.items():
        if isinstance(sqlalchemy_type, sa_type):
            return py_type
    return "unknown"  # Default fallback