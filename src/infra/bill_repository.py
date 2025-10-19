from src.domain.ports.bill_repository_port import IBillRepository
from src.domain.bill import Bill
from src.infra.db_memory import bills


class BillRepository(IBillRepository):
    def create(self, bill: Bill) -> int:
        new_id_bill = len(bills) + 1
        bills[new_id_bill] = bill
        return new_id_bill

    def get(self, id_bill: int) -> Bill:
        return bills.get(id_bill)

    def list(self):
        return bills

    def delete(self, id_bill: int) -> bool:
        if id_bill in bills:
            del bills[id_bill]
            return True
        return False

    def update(self, id_bill: int, bill: Bill) -> bool:
        if id_bill in bills:
            bills[id_bill] = bill
            return True
        return False

    def count(self) -> int:
        return len(bills)
