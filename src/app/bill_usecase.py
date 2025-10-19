from src.domain.bill import Bill
from src.domain.ports.bill_repository_port import IBillRepository
from src.app.dtos.bill_dto import BillDTO
from src.app.exceptions import InvalidBillDataError, BillNotFoundError


class BillUseCase:
    def __init__(self, repository: IBillRepository):
        self.repository = repository

    def create_bill(self, bill_data: BillDTO):
        if not all(
            [
                bill_data.name,
                bill_data.description,
                bill_data.date,
                bill_data.value,
                bill_data.situation,
            ]
        ):
            raise InvalidBillDataError("Todos os campos são obrigatórios")

        bill = Bill(
            name=bill_data.name,
            description=bill_data.description,
            date=bill_data.date,
            value=bill_data.value,
            situation=bill_data.situation,
        )
        new_id_bill = self.repository.create(bill)
        return {"id": new_id_bill, "message": "Conta cadastrada com sucesso!"}

    def get_bill(self, id_bill: int):
        bill = self.repository.get(id_bill)
        if bill:
            return bill.__dict__
        raise BillNotFoundError("ID de conta inexistente.")

    def get_bills(self):
        return {id_: bill.__dict__ for id_, bill in self.repository.list().items()}

    def delete_bill(self, id_bill):
        sucess = self.repository.delete(id_bill)
        if sucess:
            return {"message": "Conta apagada com sucesso."}
        raise BillNotFoundError("ID de conta inexistente!")

    def update_bill(self, id_bill: int, bill_data: BillDTO):
        bill = Bill(
            name=bill_data.name,
            description=bill_data.description,
            date=bill_data.date,
            value=bill_data.value,
            situation=bill_data.situation,
        )
        sucess = self.repository.update(id_bill, bill)
        if sucess:
            return {"message": "Conta atualizada com sucesso!!"}
        raise BillNotFoundError("ID de conta inexiste..")

    def get_bill_count(self) -> int:
        return self.repository.count()
