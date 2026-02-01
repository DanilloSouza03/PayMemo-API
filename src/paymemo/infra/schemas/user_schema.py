from pydantic import BaseModel
from typing import Optional
from uuid import UUID


class UserSchema(BaseModel):
    id: Optional[UUID] = None
    name: str
    email: str
    password: str
    phone: Optional[str] = None
