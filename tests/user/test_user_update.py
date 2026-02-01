import pytest
from paymemo.app.exceptions import InvalidUserDataError, UserNotFoundError


def test_update_user_success(
    user_use_case, mock_user_repository, make_user_domain, make_user_dto
):
    user = make_user_domain()
    mock_user_repository.get.return_value = user
    mock_user_repository.check_duplicate_email.return_value = False
    mock_user_repository.check_duplicate_phone.return_value = False
    mock_user_repository.update.return_value = True

    updated_data = make_user_dto(id=user.id, name="Updated")

    result = user_use_case.update_user(user.id, updated_data)

    assert result["message"] == "Usuário atualizado com sucesso!"
    mock_user_repository.update.assert_called_once()


def test_update_user_not_found(user_use_case, mock_user_repository, make_user_dto):
    mock_user_repository.get.return_value = None

    with pytest.raises(UserNotFoundError):
        user_use_case.update_user("invalid-id", make_user_dto())


def test_update_user_duplicate_email(
    user_use_case, mock_user_repository, make_user_domain, make_user_dto
):
    user = make_user_domain(email="old@email.com")
    mock_user_repository.get.return_value = user
    mock_user_repository.check_duplicate_email.return_value = True

    updated_data = make_user_dto(id=user.id, email="new@email.com")

    with pytest.raises(InvalidUserDataError, match="E-mail já cadastrado"):
        user_use_case.update_user(user.id, updated_data)


def test_update_user_duplicate_phone(
    user_use_case, mock_user_repository, make_user_domain, make_user_dto
):
    user = make_user_domain(phone="123")
    mock_user_repository.get.return_value = user
    mock_user_repository.check_duplicate_phone.return_value = True

    updated_data = make_user_dto(id=user.id, phone="999")

    with pytest.raises(InvalidUserDataError, match="Telefone já cadastrado"):
        user_use_case.update_user(user.id, updated_data)
