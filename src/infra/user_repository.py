from src.domain.ports.user_repository_port import IUserRepository
from src.domain.user import User
from typing import Optional, Dict
from src.infra.db_memory import users
from uuid import uuid4, UUID


class UserRepository(IUserRepository):
    def create(self, user: User) -> UUID:
        user.id = uuid4()
        users[user.id] = user
        return user.id

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
