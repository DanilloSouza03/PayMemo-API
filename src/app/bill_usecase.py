from src.domain.bill import Bill
from src.domain.ports.bill_repository_port import IBillRepository
from fastapi import HTTPException


class BillUseCase:
    def __init__(self, repository: IBillRepository):
        self.repository = repository

    def create_bill(self, bill_data):
        if not all(
            [
                bill_data["name"],
                bill_data["description"],
                bill_data["date"],
                bill_data["value"],
                bill_data["situation"],
            ]
        ):
            raise HTTPException(
                status_code=422, detail="Todos os campos são obrigatórios"
            )
        bill = Bill(**bill_data)
        new_id_bill = self.repository.create(bill)
        return {"id": new_id_bill, "message": "Conta cadastrada com sucesso!"}

    def get_bill(self, id_bill: int):
        bill = self.repository.get(id_bill)
        if bill:
            return bill.__dict__
        return {"erro": "ID de conta inexistente."}

    def get_bills(self):
        return {id_: bill.__dict__ for id_, bill in self.repository.list().items()}

    def delete_bill(self, id_bill):
        sucess = self.repository.delete(id_bill)
        if sucess:
            return {"message": "Conta apagada com sucesso."}
        return {"error": "ID de conta inexistente!"}

    def update_bill(self, id_bill: int, bill_data):
        bill = Bill(**bill_data)
        sucess = self.repository.update(id_bill, bill)
        if sucess:
            return {"message": "Conta atualizada com sucesso!!"}
        return {"error": "ID de conta inexiste.."}
