from paymemo.domain.ports.bill_repository_port import IBillRepository
from paymemo.domain.bill import Bill
from paymemo.infra.db_memory import bills
from typing import Dict
from uuid import UUID


class BillRepository(IBillRepository):
    def create(self, bill: Bill) -> int:
        user_bills = {
            bill_id: b for bill_id, b in bills.items() if b.user_id == bill.user_id
        }
        new_id_bill = max(bills.keys()) + 1 if bills else 1
        bills[new_id_bill] = bill
        return new_id_bill

    def get(self, id_bill: int, user_id: UUID) -> Bill:
        bill = bills.get(id_bill)
        if bill and bill.user_id == user_id:
            return bill
        return None

    def list(self, user_id: UUID) -> Dict[int, Bill]:
        return {
            bill_id: bill for bill_id, bill in bills.items() if bill.user_id == user_id
        }

    def list_all(self) -> Dict[int, Bill]:
        return bills

    def delete(self, id_bill: int, user_id: UUID) -> bool:
        bill = bills.get(id_bill)
        if bill and bill.user_id == user_id:
            del bills[id_bill]
            return True
        return False

    def update(self, id_bill: int, bill: Bill) -> bool:
        existing_bill = bills.get(id_bill)
        if existing_bill and existing_bill.user_id == bill.user_id:
            bills[id_bill] = bill
            return True
        return False

    def count(self, user_id: UUID) -> int:
        return len(self.list(user_id))
