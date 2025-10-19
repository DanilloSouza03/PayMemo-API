from src.domain.bill import Bill


def test_bill_create():
    bill = Bill(
        name="Conta do Dan",
        description="Conta para pagar o Danillo",
        date="19/10/2025",
        value=103.97,
        situation="Pago",
    )
    assert bill.name == "Conta do Dan"
    assert bill.description == "Conta para pagar o Danillo"
    assert bill.date == "19/10/2025"
    assert bill.value == 103.97
    assert bill.situation == "Pago"


def test_bill_change():
    bill = Bill(
        "Financiamento do Civic", "Parcela do carro", "25/10/2025", 985.94, "Á pagar"
    )
    bill.name = "Financiamento do Civic"
    bill.situation = "Á pagar"
    assert bill.name == "Financiamento do Civic"
    assert bill.situation == "Á pagar"
