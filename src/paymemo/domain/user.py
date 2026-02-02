from typing import Optional
from uuid import UUID, uuid4


class User:
    def __init__(
        self,
        id: Optional[UUID] = None,
        name: str = "",
        email: str = "",
        password: str = "",
        phone: Optional[str] = None,
    ):
        self.id = id or uuid4()
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
