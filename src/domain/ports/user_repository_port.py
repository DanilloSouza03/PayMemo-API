from abc import ABC, abstractmethod
from typing import Optional, Dict
from uuid import UUID
from src.domain.user import User


class IUserRepository(ABC):
    @abstractmethod
    def create(self, user: User) -> UUID:
        pass

    @abstractmethod
    def get(self, id: UUID) -> Optional[User]:
        pass

    @abstractmethod
    def update(self, id: UUID, user: User) -> bool:
        pass

    @abstractmethod
    def delete(self, id: UUID) -> bool:
        pass

    @abstractmethod
    def list(self) -> Dict[UUID, User]:
        pass
