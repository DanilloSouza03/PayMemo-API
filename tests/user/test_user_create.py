import pytest
from paymemo.app.exceptions import InvalidUserDataError


def test_create_user_success(user_use_case, mock_user_repository, make_user_dto):
    mock_user_repository.check_duplicate_email.return_value = False
    mock_user_repository.check_duplicate_phone.return_value = False
    mock_user_repository.create.return_value = 1

    result = user_use_case.create_user(make_user_dto())

    assert result["message"] == "Usuário cadastrado com sucesso!"
    mock_user_repository.create.assert_called_once()


@pytest.mark.parametrize(
    "field,value",
    [
        ("name", ""),
        ("email", ""),
        ("password", ""),
    ],
)
def test_create_user_missing_fields(user_use_case, make_user_dto, field, value):
    dto = make_user_dto(**{field: value})

    with pytest.raises(InvalidUserDataError):
        user_use_case.create_user(dto)


def test_create_user_invalid_email(user_use_case, make_user_dto):
    dto = make_user_dto(email="email_invalido")

    with pytest.raises(InvalidUserDataError, match="Formato de e-mail inválido"):
        user_use_case.create_user(dto)


def test_create_user_duplicate_email(
    user_use_case, mock_user_repository, make_user_dto
):
    mock_user_repository.check_duplicate_email.return_value = True
    mock_user_repository.check_duplicate_phone.return_value = False

    with pytest.raises(InvalidUserDataError, match="E-mail já cadastrado"):
        user_use_case.create_user(make_user_dto())


def test_create_user_duplicate_phone(
    user_use_case, mock_user_repository, make_user_dto
):
    mock_user_repository.check_duplicate_email.return_value = False
    mock_user_repository.check_duplicate_phone.return_value = True

    with pytest.raises(InvalidUserDataError, match="Telefone já cadastrado"):
        user_use_case.create_user(make_user_dto())
