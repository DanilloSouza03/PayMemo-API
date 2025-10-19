from abc import ABC, abstractmethod
from typing import Dict
from src.domain.bill import Bill


class IBillRepository(ABC):
    @abstractmethod
    def create(self, bill: Bill) -> int:
        pass

    @abstractmethod
    def get(self, id_bill: int) -> Bill:
        pass

    @abstractmethod
    def list(self) -> Dict[int, Bill]:
        pass

    @abstractmethod
    def delete(self, id_bill: int) -> bool:
        pass

    @abstractmethod
    def update(self, bill: Bill) -> bool:
        pass

    @abstractmethod
    def count(self) -> int:
        pass
