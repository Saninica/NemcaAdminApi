from pydantic import BaseModel
from .user import UserRead
from typing import Optional


class Token(BaseModel):
    access_token: str
    token_type: str
    user: UserRead

class TokenData(BaseModel):
    username: Optional[str] = None