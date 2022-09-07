import pytest
import random

from model.iban import Iban


@pytest.fixture
def iban_good_account():
    # IBAN numbers generated via http://randomiban.com/
    accounts = [
        "MC793903645089C80JGA29MY747",
        "LU608781YS8E20B1G520",
        "SE1244572683153012814280",
        "AD83963439788LN1SY39F68A",
        "GB70CAOA69329525281525",
        "SK4842092062071199678120",
        "FI1463076932834004",
        "FR320486799495M497I9K415398",
    ]

    return random.choice(accounts)


@pytest.fixture
def iban_bad_account_country():
    # IBAN numbers generated via http://randomiban.com/
    # Altered manually
    accounts = [
        "QQ29VHAV322929767755897869423",
        "TA14873287923531987386761412",
        "GZ96BARC20038445256154",
    ]

    return random.choice(accounts)


@pytest.fixture
def iban_bad_account_check_digits():
    # IBAN numbers generated via http://randomiban.com/
    # Altered manually and original check digits preserved for validation
    accounts = [
        {"account": "NI52DYVJ256334521639641427629454", "digits": "50"},
        {"account": "LI1408800614974521843", "digits": "10"},
        {"account": "EG8167898756712364521861866", "digits": "71"},
        {"account": "BH53VQDT68642863462491", "digits": "58"},
        {"account": "CV80956234173532527851788", "digits": "89"},
        {"account": "HN12QFTZ43126841519269975569", "digits": "52"},
        {"account": "KZ395963268893676339", "digits": "89"},
    ]

    return random.choice(accounts)


def test_existing_country(iban_good_account):
    iban = Iban(iban_good_account)

    assert iban.belongs_to_country()
    assert iban.is_correct()


def test_non_existing_country(iban_bad_account_country):
    iban = Iban(iban_bad_account_country)

    assert not iban.belongs_to_country()
    assert not iban.is_correct()


def test_check_digits(iban_good_account):
    iban_check_digits = iban_good_account[2:4]

    iban = Iban(iban_good_account)

    assert iban_check_digits == iban.generate_check_digits()
    assert iban.is_correct()


def test_invalid_check_digits(iban_bad_account_check_digits):
    iban_bad_account = iban_bad_account_check_digits["account"]
    iban_bad_check_digits = iban_bad_account[2:4]

    iban = Iban(iban_bad_account)
    iban_check_digits = iban.generate_check_digits()

    assert iban_bad_account_check_digits["digits"] == iban_check_digits
    assert iban_bad_check_digits != iban_check_digits
    assert iban.is_correct()
