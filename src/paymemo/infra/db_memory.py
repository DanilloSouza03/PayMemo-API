from typing import Dict
from uuid import UUID
from paymemo.domain.bill import Bill
from paymemo.domain.user import User

# Banco em memória / Database "fake"

# table bills
bills: Dict[int, Bill] = {}

# Table users
users: Dict[UUID, User] = {}
