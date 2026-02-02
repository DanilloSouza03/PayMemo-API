from paymemo.domain.bill import Bill

USER_ID = "fdad3a69-788f-433f-afff-4997e68dc919"


def test_bill_create():
    bill = Bill(
        name="Conta do Dan",
        description="Conta para pagar o Danillo",
        date="19/10/2025",
        value=103.97,
        situation="Pago",
        user_id=USER_ID,
    )
    assert bill.name == "Conta do Dan"
    assert bill.description == "Conta para pagar o Danillo"
    assert bill.date == "19/10/2025"
    assert bill.value == 103.97
    assert bill.situation == "Pago"
    assert bill.user_id == USER_ID


def test_bill_change():
    bill = Bill(
        "Financiamento do Civic",
        "Parcela do carro",
        "25/10/2025",
        985.94,
        "Á pagar",
        USER_ID,
    )
    bill.name = "Financiamento do Civic"
    bill.situation = "Á pagar"
    assert bill.name == "Financiamento do Civic"
    assert bill.situation == "Á pagar"
