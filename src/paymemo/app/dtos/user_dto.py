from typing import Optional
from uuid import UUID, uuid4


class UserDTO:
    def __init__(
        self,
        name: str,
        email: str,
        password: str,
        phone: Optional[int] = None,
        id: Optional[UUID] = None,
    ):
        self.id = id or uuid4()
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
