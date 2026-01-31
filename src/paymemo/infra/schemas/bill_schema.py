from pydantic import BaseModel
from uuid import UUID


class BillSchema(BaseModel):
    name: str
    description: str
    date: str
    value: float
    situation: str
    user_id: UUID
