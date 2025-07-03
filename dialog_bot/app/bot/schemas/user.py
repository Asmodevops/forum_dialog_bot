from typing import Optional
from pydantic import BaseModel


class UserSchema(BaseModel):
    telegram_id: int
    first_name: str
    last_name: Optional[str]
    full_name: str
    username: Optional[str]
