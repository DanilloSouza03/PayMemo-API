from src.domain.user import User
from src.domain.ports.user_repository_port import IUserRepository
from src.app.exceptions import InvalidUserDataError, UserNotFoundError
from src.app.dtos.user_dto import UserDTO
from uuid import UUID


class UserUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def create_user(self, user: UserDTO):
        if not all(
            [
                user.name,
                user.email,
                user.password,
            ]
        ):
            raise InvalidUserDataError("Faltam dados obrigátorios...")

        user = User(
            name=user.name,
            email=user.email,
            password=user.password,
            phone=user.phone,
            id=user.id,
        )

        new_user = self.repository.create(user)
        return {"id": new_user, "message": "Usuário cadastrado com sucesso!"}

    def get_user(self, id_user: UUID):
        user = self.repository.get(id_user)
        if user:
            return user.__dict__
        raise UserNotFoundError("ID de usuário inexistente.")

    def get_users(self):
        return {str(id_): user.__dict__ for id_, user in self.repository.list().items()}

    def delete_user(self, id_user: UUID):
        success = self.repository.delete(id_user)
        if success:
            return {"message": "Usuário apagado com sucesso..."}
        raise UserNotFoundError("ID de usuário errado ou não existe!")

    def update_user(self, id_user: UUID, user: UserDTO):
        if not all(
            [
                user.name,
                user.email,
                user.password,
            ]
        ):
            raise InvalidUserDataError("Faltam dados obrigatórios.")

        user = User(
            name=user.name,
            email=user.email,
            password=user.password,
            phone=user.phone,
            id=id_user,
        )
        success = self.repository.update(id_user, user)
        if success:
            return {"message": "Usuário atualizado com sucesso!"}
        raise UserNotFoundError("ID de usuário inexistente.")
