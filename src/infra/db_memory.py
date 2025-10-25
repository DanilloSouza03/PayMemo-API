from typing import Dict
from uuid import UUID
from src.domain.bill import Bill
from src.domain.user import User

# Banco em memória / Database "fake"

# table bills
bills: Dict[int, Bill] = {}

# Table users
users: Dict[UUID, User] = {}
