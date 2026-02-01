import pytest
from paymemo.app.exceptions import UserNotFoundError


def test_get_user_success(user_use_case, mock_user_repository, make_user_domain):
    user = make_user_domain()
    mock_user_repository.get.return_value = user

    result = user_use_case.get_user(user.id)

    assert result == user.__dict__
    mock_user_repository.get.assert_called_once_with(user.id)


def test_get_user_not_found(user_use_case, mock_user_repository):
    mock_user_repository.get.return_value = None

    with pytest.raises(UserNotFoundError):
        user_use_case.get_user("invalid-id")
