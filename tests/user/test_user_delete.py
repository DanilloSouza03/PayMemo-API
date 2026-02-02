import pytest
from paymemo.app.exceptions import UserNotFoundError


def test_delete_user_success(user_use_case, mock_user_repository):
    mock_user_repository.delete.return_value = True

    result = user_use_case.delete_user("user-id")

    assert result["message"] == "Usuário apagado com sucesso..."
    mock_user_repository.delete.assert_called_once()


def test_delete_user_not_found(user_use_case, mock_user_repository):
    mock_user_repository.delete.return_value = False

    with pytest.raises(UserNotFoundError):
        user_use_case.delete_user("invalid-id")
