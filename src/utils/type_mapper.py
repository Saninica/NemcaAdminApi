from sqlalchemy import (
    Integer, String, Boolean, DateTime, Float, Text, Date, Time, Numeric, LargeBinary, Enum, JSON
)
from sqlalchemy.dialects.postgresql import ARRAY
from sqlalchemy.types import TypeEngine

# Define a mapping from SQLAlchemy types to UI input types
TYPE_MAPPING = {
    Integer: "number",
    String: "text", 
    Boolean: "checkbox",
    DateTime: "datetime-local",
    Float: "number",
    Text: "textarea",
    Date: "date",
    Time: "time",
    Numeric: "number",
    LargeBinary: "file",
    Enum: "select",
    JSON: "textarea",
    ARRAY: "textarea",
    # Add more mappings as needed
}

def map_type(sqlalchemy_type: TypeEngine) -> dict:
    """
    Map SQLAlchemy type to UI input type with additional metadata
    """
    input_type = "text"  # Default fallback
    constraints = {}
    
    for sa_type, ui_type in TYPE_MAPPING.items():
        if isinstance(sqlalchemy_type, sa_type):
            input_type = ui_type
            break
    
    # Add specific constraints based on type
    if isinstance(sqlalchemy_type, String):
        if hasattr(sqlalchemy_type, 'length') and sqlalchemy_type.length:
            constraints['maxLength'] = sqlalchemy_type.length
            
        # Check if it's likely an email field
        if hasattr(sqlalchemy_type, 'name') and 'email' in str(sqlalchemy_type).lower():
            input_type = "email"
            constraints['pattern'] = r'^[^\s@]+@[^\s@]+\.[^\s@]+$'
            
        # Check if it's likely a URL field
        elif hasattr(sqlalchemy_type, 'name') and 'url' in str(sqlalchemy_type).lower():
            input_type = "url"
            
        # Check if it's likely a password field
        elif hasattr(sqlalchemy_type, 'name') and 'password' in str(sqlalchemy_type).lower():
            input_type = "password"
            
    elif isinstance(sqlalchemy_type, Integer):
        constraints['step'] = 1
        
    elif isinstance(sqlalchemy_type, Float):
        constraints['step'] = 0.01
        
    elif isinstance(sqlalchemy_type, Numeric):
        constraints['step'] = 0.01
        if hasattr(sqlalchemy_type, 'precision') and sqlalchemy_type.precision:
            constraints['precision'] = sqlalchemy_type.precision
        if hasattr(sqlalchemy_type, 'scale') and sqlalchemy_type.scale:
            constraints['scale'] = sqlalchemy_type.scale
    
    return {
        "input_type": input_type,
        "constraints": constraints
    }