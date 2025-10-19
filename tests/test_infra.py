import pytest
from src.infra.bill_repository import BillRepository
from src.infra.db_memory import bills
from src.domain.bill import Bill


@pytest.fixture(autouse=True)
def clear_bills_db():

    bills.clear()
    yield
    bills.clear()


@pytest.fixture
def bill_repository():
    return BillRepository()


def test_create_bill(bill_repository):
    bill = Bill("Aluguel da Casa", "Mensal", "01/09/2025", 1578.53, "Á pagar")
    bill_id = bill_repository.create(bill)
    assert bill_id == 1
    assert 1 in bills
    assert bills[1].name == "Aluguel da Casa"


def test_get_bill_existing(bill_repository):
    bill = Bill("Internet", "Mensal", "08/11/2025", 99.90, "Á pagar")
    bill_repository.create(bill)
    retrieved_bill = bill_repository.get(1)
    assert retrieved_bill is not None
    assert retrieved_bill.name == "Internet"


def test_get_bill_non_existing(bill_repository):
    retrieved_bill = bill_repository.get(99)
    assert retrieved_bill is None


def test_list_bills_empty(bill_repository):
    all_bills = bill_repository.list()
    assert len(all_bills) == 0


def test_list_bills_with_data(bill_repository):
    bill_repository.create(Bill("Luz", "Energia", "11/01/2025", 120.00, "Á pagar"))
    bill_repository.create(Bill("Água", "Consumo", "07/01/2025", 50.00, "Pago"))
    all_bills = bill_repository.list()
    assert len(all_bills) == 2
    assert 1 in all_bills
    assert 2 in all_bills


def test_delete_bill_existing(bill_repository):
    bill_repository.create(Bill("Gás", "Cozinha", "30/01/2025", 80.00, "Á pagar"))
    success = bill_repository.delete(1)
    assert success is True
    assert 1 not in bills


def test_delete_bill_non_existing(bill_repository):
    success = bill_repository.delete(99)
    assert success is False


def test_update_bill_existing(bill_repository):
    bill_repository.create(Bill("Telefone", "Fixo", "25/01/2025", 70.00, "Á pagar"))
    updated_bill = Bill("Telefone", "Móvel", "25/01/2025", 85.00, "Pago")
    success = bill_repository.update(1, updated_bill)
    assert success is True
    assert bills[1].description == "Móvel"
    assert bills[1].value == 85.00
    assert bills[1].situation == "Pago"


def test_update_bill_non_existing(bill_repository):
    updated_bill = Bill("Inexistente", "Teste", "01/01/2025", 10.00, "Á pagar")
    success = bill_repository.update(99, updated_bill)
    assert success is False


def test_count_bills_empty(bill_repository):
    count = bill_repository.count()
    assert count == 0


def test_count_bills_with_data(bill_repository):
    bill_repository.create(Bill("Luz", "Energia", "10/01/2025", 120.00, "Á pagar"))
    bill_repository.create(Bill("Água", "Consumo", "15/01/2025", 50.00, "Pago"))
    count = bill_repository.count()
    assert count == 2
