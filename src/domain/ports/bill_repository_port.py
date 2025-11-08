from abc import ABC, abstractmethod
from typing import Dict
from uuid import UUID
from src.domain.bill import Bill


class IBillRepository(ABC):
    @abstractmethod
    def create(self, bill: Bill) -> int:
        pass

    @abstractmethod
    def get(self, id_bill: int, user_id: UUID) -> Bill:
        pass

    @abstractmethod
    def list(self, user_id: UUID) -> Dict[int, Bill]:
        pass

    @abstractmethod
    def list_all(self) -> Dict[int, Bill]:
        pass

    @abstractmethod
    def delete(self, id_bill: int, user_id: UUID) -> bool:
        pass

    @abstractmethod
    def update(self, id_bill: int, bill: Bill) -> bool:
        pass

    @abstractmethod
    def count(self, user_id: UUID) -> int:
        pass
