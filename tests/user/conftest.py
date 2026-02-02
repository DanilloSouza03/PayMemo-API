import pytest
from unittest.mock import Mock
from uuid import uuid4

from paymemo.app.user_usecase import UserUseCase
from paymemo.app.dtos.user_dto import UserDTO
from paymemo.domain.user import User
from paymemo.domain.ports.user_repository_port import IUserRepository


@pytest.fixture
def mock_user_repository():
    return Mock(spec=IUserRepository)


@pytest.fixture
def user_use_case(mock_user_repository):
    return UserUseCase(mock_user_repository)


@pytest.fixture
def make_user_dto():
    def _make(**overrides):
        data = {
            "id": uuid4(),
            "name": "Test User",
            "email": "test@example.com",
            "password": "password123",
            "phone": "1234567890",
        }
        data.update(overrides)
        return UserDTO(**data)

    return _make


@pytest.fixture
def make_user_domain(make_user_dto):
    def _make(**overrides):
        dto = make_user_dto(**overrides)
        return User(
            id=dto.id,
            name=dto.name,
            email=dto.email,
            password=dto.password,
            phone=dto.phone,
        )

    return _make
