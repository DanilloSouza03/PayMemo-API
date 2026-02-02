import pytest
from unittest.mock import MagicMock
from paymemo.app.bill_usecase import BillUseCase
from paymemo.app.dtos.bill_dto import BillDTO
from paymemo.app.exceptions import InvalidBillDataError, BillNotFoundError
from paymemo.domain.bill import Bill


USER_ID = "fdad3a69-788f-433f-afff-4997e68dc919"


@pytest.fixture
def bill_repository_mock():
    return MagicMock()


@pytest.fixture
def user_repository_mock():
    return MagicMock()


@pytest.fixture
def bill_use_case(bill_repository_mock, user_repository_mock):
    return BillUseCase(
        bill_repository=bill_repository_mock, user_repository=user_repository_mock
    )


def test_creat_bill_success(bill_use_case, bill_repository_mock, user_repository_mock):
    bill_dto = BillDTO(
        "Spotify Premium",
        "Conta do Spotify para baixar músicas",
        "19/11/2025",
        19.99,
        "Pago",
        USER_ID,
    )

    user_repository_mock.get.return_value = True

    bill_repository_mock.create.return_value = 1

    result = bill_use_case.create_bill(bill_dto)

    user_repository_mock.get.assert_called_once_with(bill_dto.user_id)
    bill_repository_mock.create.assert_called_once()
    assert result == {"id": 1, "message": "Conta cadastrada com sucesso!"}


def test_create_bill_invalid_data(
    bill_use_case, bill_repository_mock, user_repository_mock
):
    bill_dto = BillDTO(
        "",
        "Mensalidade",
        "09/02/2025",
        99.90,
        "Á pagar",
        USER_ID,
    )

    with pytest.raises(InvalidBillDataError) as exc_info:
        bill_use_case.create_bill(bill_dto)
    assert str(exc_info.value) == "Todos os campos são obrigatórios"
    bill_repository_mock.create.assert_not_called()


def test_get_bill_success(bill_use_case, bill_repository_mock, user_repository_mock):
    mock_bill = Bill(
        "Água",
        "Consumo",
        "17/07/2025",
        50.00,
        "Á pagar",
        USER_ID,
    )

    bill_repository_mock.get.return_value = mock_bill

    result = bill_use_case.get_bill(1, USER_ID)

    bill_repository_mock.get.assert_called_once_with(1, USER_ID)
    assert result == mock_bill.__dict__


def test_get_bill_not_found(bill_use_case, bill_repository_mock):
    bill_repository_mock.get.return_value = None

    with pytest.raises(BillNotFoundError) as exc_info:
        bill_use_case.get_bill(99, USER_ID)
    assert str(exc_info.value) == "ID de conta inexistente ou não pertence ao usuário."
    bill_repository_mock.get.assert_called_once_with(99, USER_ID)


def test_get_bills_success(bill_use_case, bill_repository_mock):
    mock_bills_data = {
        1: Bill(
            "Luz",
            "Energia",
            "22/02/2025",
            126.58,
            "Á pagar",
            USER_ID,
        ),
        2: Bill(
            "Gás",
            "Cozinha",
            "30/02/2025",
            84.81,
            "Pago",
            USER_ID,
        ),
    }
    bill_repository_mock.list.return_value = mock_bills_data

    result = bill_use_case.get_bills(USER_ID)

    bill_repository_mock.list.assert_called_once()
    expected_result = {id_: bill.__dict__ for id_, bill in mock_bills_data.items()}
    assert result == expected_result


def test_delete_bill_success(bill_use_case, bill_repository_mock):
    bill_repository_mock.delete.return_value = True

    result = bill_use_case.delete_bill(1, USER_ID)

    bill_repository_mock.delete.assert_called_once_with(1, USER_ID)
    assert result == {"message": "Conta apagada com sucesso."}


def test_delete_bill_not_found(bill_use_case, bill_repository_mock):
    bill_repository_mock.delete.return_value = False

    with pytest.raises(BillNotFoundError) as exc_info:
        bill_use_case.delete_bill(99, USER_ID)
    assert str(exc_info.value) == "ID de conta inexistente ou não pertence ao usuário!"
    bill_repository_mock.delete.assert_called_once_with(99, USER_ID)


def test_update_bill_success(bill_use_case, bill_repository_mock, user_repository_mock):
    bill_dto = BillDTO(
        "Telefone",
        "Celular",
        "01/03/2025",
        36.46,
        "Pago",
        USER_ID,
    )
    user_repository_mock.get.return_value = True
    bill_repository_mock.update.return_value = True

    result = bill_use_case.update_bill(1, bill_dto)

    user_repository_mock.get.assert_called_once_with(USER_ID)
    bill_repository_mock.update.assert_called_once()
    assert result == {"message": "Conta atualizada com sucesso!!"}


def test_update_bill_not_found(bill_use_case, bill_repository_mock):
    bill_dto = BillDTO(
        "Telefone",
        "Fixo",
        "01/03/2025",
        36.46,
        "Pago",
        USER_ID,
    )
    bill_repository_mock.update.return_value = False

    with pytest.raises(BillNotFoundError) as exc_info:
        bill_use_case.update_bill(99, bill_dto)
    assert str(exc_info.value) == "ID de conta inexistente ou não pertence ao usuário."
    bill_repository_mock.update.assert_called_once()


def test_get_bill_count(bill_use_case, bill_repository_mock):
    bill_repository_mock.count.return_value = 5

    result = bill_use_case.get_bill_count(USER_ID)

    bill_repository_mock.count.assert_called_once()
    assert result == 5
