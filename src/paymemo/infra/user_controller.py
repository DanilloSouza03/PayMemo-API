from fastapi import APIRouter, HTTPException, status, Depends
from paymemo.infra.schemas.user_schema import UserSchema
from paymemo.infra.user_repository import UserRepository
from paymemo.app.user_usecase import UserUseCase
from paymemo.app.dtos.user_dto import UserDTO
from paymemo.app.exceptions import InvalidUserDataError, UserNotFoundError
from uuid import UUID


def get_user_use_case() -> UserUseCase:
    repository = UserRepository()
    return UserUseCase(repository)


router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/criarUsuario/")
def create_user_endpoint(
    user: UserSchema, use_case: UserUseCase = Depends(get_user_use_case)
):
    try:
        user_dto = UserDTO(**user.model_dump())
        return use_case.create_user(user_dto)
    except InvalidUserDataError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e)
        )


@router.get("/pegarUsuario/{id_user}")
def get_user_endpoint(
    id_user: UUID, use_case: UserUseCase = Depends(get_user_use_case)
):
    try:
        return use_case.get_user(id_user)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.get("/listarUsuarios/")
def get_users_endpoint(use_case: UserUseCase = Depends(get_user_use_case)):
    return use_case.get_users()


@router.delete("/deletarUsuario/{id_user}")
def delete_user_endpoint(
    id_user: UUID, use_case: UserUseCase = Depends(get_user_use_case)
):
    try:
        return use_case.delete_user(id_user)
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))


@router.put("/atualizarUsuario/{id_user}")
def update_user_endpoint(
    id_user: UUID, user: UserSchema, use_case: UserUseCase = Depends(get_user_use_case)
):
    try:
        user_dto = UserDTO(**user.model_dump())
        return use_case.update_user(id_user, user_dto)
    except InvalidUserDataError as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_CONTENT, detail=str(e)
        )
    except UserNotFoundError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
