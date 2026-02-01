from paymemo.domain.bill import Bill
from paymemo.domain.ports.bill_repository_port import IBillRepository
from paymemo.domain.ports.user_repository_port import (
    IUserRepository,
)
from paymemo.app.dtos.bill_dto import BillDTO
from paymemo.app.exceptions import (
    InvalidBillDataError,
    BillNotFoundError,
    UserNotFoundError,
)
from uuid import UUID


class BillUseCase:
    def __init__(
        self, bill_repository: IBillRepository, user_repository: IUserRepository
    ):
        self.repository = bill_repository
        self.user_repository = user_repository

    def create_bill(self, bill_data: BillDTO):
        if not all(
            [
                bill_data.name,
                bill_data.description,
                bill_data.date,
                bill_data.value,
                bill_data.situation,
                bill_data.user_id,
            ]
        ):
            raise InvalidBillDataError("Todos os campos são obrigatórios")

        if not self.user_repository.get(bill_data.user_id):
            raise UserNotFoundError(
                "User ID não encontrado. Não é possível criar a conta."
            )

        bill = Bill(
            name=bill_data.name,
            description=bill_data.description,
            date=bill_data.date,
            value=bill_data.value,
            situation=bill_data.situation,
            user_id=bill_data.user_id,
        )
        new_id_bill = self.repository.create(bill)
        return {"id": new_id_bill, "message": "Conta cadastrada com sucesso!"}

    def get_bill(self, id_bill: int, user_id: UUID):
        bill = self.repository.get(id_bill, user_id)
        if bill:
            return bill.__dict__
        raise BillNotFoundError("ID de conta inexistente ou não pertence ao usuário.")

    def get_bills(self, user_id: UUID):
        if not self.user_repository.get(user_id):
            raise UserNotFoundError("User ID não encontrado.")
        return {
            id_: bill.__dict__ for id_, bill in self.repository.list(user_id).items()
        }

    def get_all_bills(self):
        return {id_: bill.__dict__ for id_, bill in self.repository.list_all().items()}

    def delete_bill(self, id_bill: int, user_id: UUID):
        sucess = self.repository.delete(id_bill, user_id)
        if sucess:
            return {"message": "Conta apagada com sucesso."}
        raise BillNotFoundError("ID de conta inexistente ou não pertence ao usuário!")

    def update_bill(self, id_bill: int, bill_data: BillDTO):
        if not bill_data.user_id:
            raise InvalidBillDataError("User ID é obrigatório para atualização.")

        if not self.user_repository.get(bill_data.user_id):

            raise UserNotFoundError(
                "User ID não encontrado. Não é possível atualizar a conta."
            )

        bill = Bill(
            name=bill_data.name,
            description=bill_data.description,
            date=bill_data.date,
            value=bill_data.value,
            situation=bill_data.situation,
            user_id=bill_data.user_id,
        )
        sucess = self.repository.update(id_bill, bill)
        if sucess:
            return {"message": "Conta atualizada com sucesso!!"}
        raise BillNotFoundError("ID de conta inexistente ou não pertence ao usuário.")

    def get_bill_count(self, user_id: UUID) -> int:
        if not self.user_repository.get(user_id):
            raise UserNotFoundError("User ID não encontrado.")
        return self.repository.count(user_id)
