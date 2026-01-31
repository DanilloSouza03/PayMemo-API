import re
from paymemo.domain.user import User
from paymemo.domain.ports.user_repository_port import IUserRepository
from paymemo.app.exceptions import InvalidUserDataError, UserNotFoundError
from paymemo.app.dtos.user_dto import UserDTO
from uuid import UUID


class UserUseCase:
    def __init__(self, repository: IUserRepository):
        self.repository = repository

    def _validate_user_data(self, user_data: UserDTO):
        if not all(
            [
                user_data.name,
                user_data.email,
                user_data.password,
            ]
        ):
            raise InvalidUserDataError("Faltam dados obrigátorios.")

        # Validar formato de e-mail
        email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"
        if not re.match(email_regex, user_data.email):
            raise InvalidUserDataError("Formato de e-mail inválido.")

    def create_user(self, user_data: UserDTO):
        self._validate_user_data(user_data)

        user = User(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password,
            phone=user_data.phone,
            id=user_data.id,
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

    def update_user(self, id_user: UUID, user_data: UserDTO):
        self._validate_user_data(user_data)

        user = User(
            name=user_data.name,
            email=user_data.email,
            password=user_data.password,
            phone=user_data.phone,
            id=id_user,
        )
        success = self.repository.update(id_user, user)
        if success:
            return {"message": "Usuário atualizado com sucesso!"}
        raise UserNotFoundError("ID de usuário inexistente.")
