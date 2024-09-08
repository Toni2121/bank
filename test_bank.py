import bank
import datetime


def test_bank_perform_trx_empty():
    bank.perform_trx(1001)
    assert len(bank.bank_accounts[1001]["transactions_to_execute"]) == 0


def test_perform_trx_added_to_history():
    bank.perform_trx(1001)
    assert len(bank.bank_accounts[1001]["transaction_history"]) == 3
    assert bank.bank_accounts[1001]["transaction_history"][1][2] == 1002
    assert bank.bank_accounts[1001]["transaction_history"][2][2] == 1003


def test_perform_trx_decrease():
    assert bank.bank_accounts[1001]["balance"] == 2500.50 - 300 - 200


def test_perform_trx_increase():
    assert bank.bank_accounts[1002]["balance"] == 3900.75 + 300
    assert bank.bank_accounts[1003]["balance"] == 3100.75 + 200


def test_create_trx():
    bank.create_trx(1001, 1002, 300)
    trx = bank.bank_accounts[1001]["transactions_to_execute"][0]
    assert len(bank.bank_accounts[1001]["transactions_to_execute"]) == 1
    assert trx[1] == 1001
    assert trx[2] == 1002
    assert trx[3] == 300
    assert datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')[:19] == trx[0][:19]


def test_name_by_get():
    result = bank.get_by_name(bank.bank_accounts, "bo")
    expected = {
        1002: {
            "first_name": "Bob",
            "last_name": "Johnson",
            "id_number": "987654321",
            "balance": 4200.75,
            "transactions_to_execute": [],
            "transaction_history": []
        },
        1003: {
            "first_name": "Bob2",
            "last_name": "Johnson2",
            "id_number": "987654320",
            "balance": 3300.75,
            "transactions_to_execute": [],
            "transaction_history": []
        }
    }
    assert result == expected, f"Expected {expected}, but got {result}"
