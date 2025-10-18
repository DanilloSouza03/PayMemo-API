from pydantic import BaseModel


class BillSchema(BaseModel):
    name: str
    description: str
    date: str
    value: float
    situation: str
