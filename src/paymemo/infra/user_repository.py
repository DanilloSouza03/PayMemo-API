from paymemo.domain.ports.user_repository_port import IUserRepository
from paymemo.domain.user import User
from typing import Optional, Dict
from paymemo.infra.db_memory import users
from uuid import uuid4, UUID


class UserRepository(IUserRepository):
    def create(self, user: User) -> UUID:
        user.id = uuid4()
        users[user.id] = user
        return user.id

    def check_duplicate_email(self, email):
        for user in users.values():
            if user.email == email:
                return True
        return False

    def check_duplicate_phone(self, phone):
        if phone is None:
            return False

        for user in users.values():
            if user.phone == phone:
                return True
        return False

    def get(self, id: UUID) -> Optional[User]:
        return users.get(id)

    def update(self, id: UUID, user: User) -> bool:
        if id in users:
            users[id] = user
            return True
        return False

    def delete(self, id: UUID):
        if id in users:
            del users[id]
            return True
        return False

    def list(self) -> Dict[UUID, User]:
        return users
