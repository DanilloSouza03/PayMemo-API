from fastapi import APIRouter
from src.infra.schemas.bill_schema import BillSchema
from src.app.bill_usecase import BillUseCase
from src.infra.bill_repository import BillRepository


repository = BillRepository()
use_case = BillUseCase(repository)

router = APIRouter()


@router.get("/")
def home():
    from src.infra.db_memory import bills

    return {
        "Bem vindos a nova PayTrack, tentando implementar uma nova arquitetura": {
            "Temos um total de contas": len(bills)
        }
    }


@router.post("/criarConta/")
def create_bill_endpoint(bill: BillSchema):
    return use_case.create_bill(bill.dict())


@router.get("/pegarConta/{id_bill}")
def get_bill_endpoint(id_bill: int):
    return use_case.get_bill(id_bill)


@router.get("/listarContas/")
def get_bills_endpoint():
    return use_case.get_bills()


@router.delete("/deletarConta/{id_bill}")
def delete_bill_endpoint(id_bill: int):
    return use_case.delete_bill(id_bill)


@router.put("/atualizarConta/{id_bill}")
def update_bill_endpoint(id_bill: int, bill: BillSchema):
    return use_case.update_bill(id_bill, bill.dict())
