from uuid import UUID


class BillDTO:
    def __init__(
        self,
        name: str,
        description: str,
        date: str,
        value: float,
        situation: str,
        user_id: UUID,
    ):
        self.name = name
        self.description = description
        self.date = date
        self.value = value
        self.situation = situation
        self.user_id = user_id
