from fastapi import APIRouter, HTTPException, status, Depends
from paymemo.infra.schemas.bill_schema import BillSchema
from paymemo.infra.bill_repository import BillRepository
from paymemo.infra.user_repository import UserRepository
from paymemo.app.bill_usecase import BillUseCase
from paymemo.app.dtos.bill_dto import BillDTO
from paymemo.app.exceptions import (
    BillNotFoundError,
    InvalidBillDataError,
    UserNotFoundError,
)
from uuid import UUID


def get_bill_use_case() -> BillUseCase:
    bill_repository = BillRepository()
    user_repository = UserRepository()
    return BillUseCase(bill_repository, user_repository)


router = APIRouter(prefix="/bill", tags=["Bills"])


@router.get("/home/{user_id}")
def home(user_id: UUID, use_case: BillUseCase = Depends(get_bill_use_case)):
    try:
        user_bills = use_case.get_bills(user_id)
        return {"message": f"Contas para o usuário {user_id}", "bills": user_bills}
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e)
        )


@router.post("/criarConta/")
def create_bill_endpoint(
    bill: BillSchema, use_case: BillUseCase = Depends(get_bill_use_case)
):
    try:
        bill_dto = BillDTO(
            name=bill.name,
            description=bill.description,
            date=bill.date,
            value=bill.value,
            situation=bill.situation,
            user_id=bill.user_id,
        )
        return use_case.create_bill(bill_dto)
    except InvalidBillDataError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e)
        )
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/pegarConta/{user_id}/{id_bill}")
def get_bill_endpoint(
    user_id: UUID, id_bill: int, use_case: BillUseCase = Depends(get_bill_use_case)
):
    try:
        return use_case.get_bill(id_bill, user_id)
    except BillNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/listarContas/")
def get_all_bills_endpoint(use_case: BillUseCase = Depends(get_bill_use_case)):
    return use_case.get_all_bills()


@router.delete("/deletarConta/{user_id}/{id_bill}")
def delete_bill_endpoint(
    user_id: UUID, id_bill: int, use_case: BillUseCase = Depends(get_bill_use_case)
):
    try:
        return use_case.delete_bill(id_bill, user_id)
    except BillNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/atualizarConta/{id_bill}")
def update_bill_endpoint(
    id_bill: int, bill: BillSchema, use_case: BillUseCase = Depends(get_bill_use_case)
):
    try:
        bill_dto = BillDTO(
            name=bill.name,
            description=bill.description,
            date=bill.date,
            value=bill.value,
            situation=bill.situation,
            user_id=bill.user_id,
        )
        return use_case.update_bill(id_bill, bill_dto)
    except InvalidBillDataError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e)
        )
    except BillNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
