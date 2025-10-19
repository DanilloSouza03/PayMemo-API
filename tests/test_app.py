import pytest
from unittest.mock import MagicMock
from src.app.bill_usecase import BillUseCase
from src.app.dtos.bill_dto import BillDTO
from src.app.exceptions import InvalidBillDataError, BillNotFoundError
from src.domain.bill import Bill


@pytest.fixture
def mock_repo():
    return MagicMock()


@pytest.fixture
def bill_use_case(mock_repo):
    return BillUseCase(mock_repo)


def test_creat_bill_success(bill_use_case, mock_repo):
    bill_dto = BillDTO(
        "Spotify Premium",
        "Conta do Spotify para baixar músicas",
        "19/11/2025",
        19.99,
        "Pago",
    )
    mock_repo.create.return_value = 1

    result = bill_use_case.create_bill(bill_dto)

    mock_repo.create.assert_called_once()
    assert result == {"id": 1, "message": "Conta cadastrada com sucesso!"}


def test_create_bill_invalid_data(bill_use_case, mock_repo):
    bill_dto = BillDTO("", "Mensalidade", "09/02/2025", 99.90, "Á pagar")

    with pytest.raises(InvalidBillDataError) as exc_info:
        bill_use_case.create_bill(bill_dto)
    assert str(exc_info.value) == "Todos os campos são obrigatórios"
    mock_repo.create.assert_not_called()


def test_get_bill_success(bill_use_case, mock_repo):
    mock_bill = Bill("Água", "Consumo", "17/07/2025", 50.00, "Á pagar")
    mock_repo.get.return_value = mock_bill

    result = bill_use_case.get_bill(1)

    mock_repo.get.assert_called_once_with(1)
    assert result == mock_bill.__dict__


def test_get_bill_not_found(bill_use_case, mock_repo):
    mock_repo.get.return_value = None

    with pytest.raises(BillNotFoundError) as exc_info:
        bill_use_case.get_bill(99)
    assert str(exc_info.value) == "ID de conta inexistente."
    mock_repo.get.assert_called_once_with(99)


def test_get_bills_success(bill_use_case, mock_repo):
    mock_bills_data = {
        1: Bill("Luz", "Energia", "22/02/2025", 126.58, "Á pagar"),
        2: Bill("Gás", "Cozinha", "30/02/2025", 84.81, "Pago"),
    }
    mock_repo.list.return_value = mock_bills_data

    result = bill_use_case.get_bills()

    mock_repo.list.assert_called_once()
    expected_result = {id_: bill.__dict__ for id_, bill in mock_bills_data.items()}
    assert result == expected_result


def test_delete_bill_success(bill_use_case, mock_repo):
    mock_repo.delete.return_value = True

    result = bill_use_case.delete_bill(1)

    mock_repo.delete.assert_called_once_with(1)
    assert result == {"message": "Conta apagada com sucesso."}


def test_delete_bill_not_found(bill_use_case, mock_repo):
    mock_repo.delete.return_value = False

    with pytest.raises(BillNotFoundError) as exc_info:
        bill_use_case.delete_bill(99)
    assert str(exc_info.value) == "ID de conta inexistente!"
    mock_repo.delete.assert_called_once_with(99)


def test_update_bill_success(bill_use_case, mock_repo):
    bill_dto = BillDTO("Telefone", "Celular", "01/03/2025", 36.46, "Pago")
    mock_repo.update.return_value = True

    result = bill_use_case.update_bill(1, bill_dto)

    mock_repo.update.assert_called_once()
    assert result == {"message": "Conta atualizada com sucesso!!"}


def test_update_bill_not_found(bill_use_case, mock_repo):
    bill_dto = BillDTO("Telefone", "Fixo", "01/03/2025", 36.46, "Pago")
    mock_repo.update.return_value = False

    with pytest.raises(BillNotFoundError) as exc_info:
        bill_use_case.update_bill(99, bill_dto)
    assert str(exc_info.value) == "ID de conta inexiste.."
    mock_repo.update.assert_called_once()


def test_get_bill_count(bill_use_case, mock_repo):
    mock_repo.count.return_value = 5

    result = bill_use_case.get_bill_count()

    mock_repo.count.assert_called_once()
    assert result == 5
