from fastapi import APIRouter
from src.utils.model_inspector import get_models_metadata
from src.utils.all_models import get_all_sqlalchemy_models
from src.schemas.model_metadata import ModelMetadata

router = APIRouter()

@router.get("/models", response_model=ModelMetadata)
async def list_models():
    models = get_all_sqlalchemy_models()
    metadata = get_models_metadata(models)
    return {"models": metadata}
