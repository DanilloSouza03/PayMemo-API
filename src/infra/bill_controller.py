from fastapi import APIRouter, HTTPException, status, Depends
from src.infra.schemas.bill_schema import BillSchema
from src.infra.bill_repository import BillRepository
from src.app.bill_usecase import BillUseCase
from src.app.dtos.bill_dto import BillDTO
from src.app.exceptions import BillNotFoundError, InvalidBillDataError


def get_bill_use_case() -> BillUseCase:
    repository = BillRepository()
    return BillUseCase(repository)


router = APIRouter()


@router.get("/")
def home(use_case: BillUseCase = Depends(get_bill_use_case)):
    count_bills = use_case.get_bill_count()

    return {
        "Bem vindos a nova PayTrack, tentando implementar uma nova arquitetura": {
            "Temos um total de contas": count_bills
        }
    }


@router.post("/criarConta/")
def create_bill_endpoint(
    bill: BillSchema, use_case: BillUseCase = Depends(get_bill_use_case)
):
    try:
        bill_dto = BillDTO(**bill.model_dump())
        return use_case.create_bill(bill_dto)
    except InvalidBillDataError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e)
        )


@router.get("/pegarConta/{id_bill}")
def get_bill_endpoint(id_bill: int, use_case: BillUseCase = Depends(get_bill_use_case)):
    try:
        return use_case.get_bill(id_bill)
    except BillNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/listarContas/")
def get_bills_endpoint(use_case: BillUseCase = Depends(get_bill_use_case)):
    return use_case.get_bills()


@router.delete("/deletarConta/{id_bill}")
def delete_bill_endpoint(
    id_bill: int, use_case: BillUseCase = Depends(get_bill_use_case)
):
    try:
        return use_case.delete_bill(id_bill)
    except BillNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/atualizarConta/{id_bill}")
def update_bill_endpoint(
    id_bill: int, bill: BillSchema, use_case: BillUseCase = Depends(get_bill_use_case)
):
    try:
        bill_dto = BillDTO(**bill.model_dump())
        return use_case.update_bill(id_bill, bill_dto)
    except InvalidBillDataError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e)
        )
    except BillNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
