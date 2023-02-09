from unittest.mock import Mock

import pytest

from app.message_consumer import MessageConsumer

TRANSACTIONS = [
    {
        "event_date_time": "2023-02-07T14:34:19.628925",
        "user_id": 0,
        "transaction_id": "e2559286-2d84-4256-8a19-d8259e451bac",
        "transaction_date": "2020-10-27 15:01:59",
        "spend_amount": -8945,
        "spend_currency": "GBP",
        "loyalty_id": "e2559286-2d84-4256-8a19-d8259e451bac",
        "mid": "test-mid-123",
        "scheme_account_id": 0,
        "encrypted_credentials": "Cl1h4vksFj/8EbTzOORVu+4yMWWS4Yvm1vs7hSzYkRZ0Y/muMuWWKHXohziGiXjOFK9dhI1hW286THYqNKJb",
        "status": "EXPORTED",
        "feed_type": "REFUND",
        "location_id": None,
        "merchant_internal_id": None,
        "payment_card_account_id": 0,
        "settlement_key": "fea4fdbfb49f9e328e57293b420f9dd36a33689f572dd19ff655918c4aeb4515",
        "authorisation_code": "444444",
        "approval_code": "",
        "loyalty_identifier": "88899966",
        "record_uid": None,
        "export_uid": "e06dbc5f-8ed3-4a49-b830-6f5e65b563ec",
    }
]


@pytest.fixture()
def message_consumer():
    connection = Mock()
    return MessageConsumer(connection=connection)


@pytest.fixture()
def audit_log_viator_404_fail():
    return {
        "provider_slug": "bpl-viator",
        "transactions": TRANSACTIONS,
        "audit_data": {
            "request": {
                "body": {
                    "id": "bpl-viator-b090fb6deaf5c629caeb406448f36a1f1c2ccb51",
                    "transaction_total": -8945,
                    "datetime": 1603810919,
                    "MID": "test-mid-123",
                    "loyalty_id": "88899966",
                    "transaction_id": "e2559286-2d84-4256-8a19-d8259e451bac",
                    "request_url": "http://localhost/viator/transaction",
                },
                "timestamp": "2023-02-07 14:34:20",
            },
            "response": {
                "body": {"code": "NO_ACTIVE_CAMPAIGNS", "display_message": "No active campaigns found for retailer."},
                "status_code": 404,
                "timestamp": "2023-02-07 14:34:20",
            },
        },
        "retry_count": 0,
    }


@pytest.fixture()
def audit_log_viator_success_200():
    return {
        "provider_slug": "bpl-viator",
        "transactions": TRANSACTIONS,
        "audit_data": {
            "request": {
                "body": {
                    "MID": "020150514",
                    "datetime": 1665646782,
                    "id": "bpl-viator-12a2e1f5f2464fe3cbd4c741f186240773c74217",
                    "loyalty_id": "9e23f43c-3e6d-43ee-80ed-458f6fd5ba3b",
                    "request_url": "http://vela-api.bpl/retailers/viator/transaction",
                    "transaction_id": "482286275826354",
                    "transaction_total": 1200,
                },
                "timestamp": "2022-10-13 07:39:44",
            },
            "response": {"body": "Awarded", "status_code": 200, "timestamp": "2022-10-13 07:39:44"},
        },
    }


@pytest.fixture()
def audit_log_squaremeal_success_200():
    return {
        "provider_slug": "squaremeal",
        "transactions": TRANSACTIONS,
        "audit_data": {
            "request": {
                "body": {
                    "auth": False,
                    "brand_id": "95062ee2-2f1c-4742-aad6-6341c7b8fd6f",
                    "cleared": False,
                    "loyalty_id": "ba3fee13-f91a-4203-8f66-c951c16e2d08",
                    "mid": "000000029949781",
                    "payment_card_account_id": 366733,
                    "payment_card_expiry_month": 11,
                    "payment_card_expiry_year": 2022,
                    "payment_card_last_four": "7005",
                    "payment_scheme": {"approval_code": "", "auth_code": "047399", "slug": "visa"},
                    "request_url": "https://uk-bink-transactions.azurewebsites.net/api/BinkTransactions",
                    "store_id": "95062ee2-2f1c-4742-aad6-6341c7b8fd6f",
                    "transaction_amount": 5000,
                    "transaction_currency": "GBP",
                    "transaction_date": "2023-01-14T10:47:39",
                    "transaction_id": "0b60537dd007c69bfbecce349087ebd3939157fa52b6b24d4427a4fff16675be",
                },
                "timestamp": "2023-01-16 14:03:31",
            },
            "response": {
                "body": "Bink Transaction details processed sucessfully!",
                "status_code": 200,
                "timestamp": "2023-01-16 14:03:33",
            },
        },
    }


@pytest.fixture()
def audit_log_wasabi_failure_200():
    return {
        "provider_slug": "wasabi-club",
        "transactions": TRANSACTIONS,
        "audit_data": {
            "request": {
                "body": {
                    "ReceiptNo": "0000A06305000120625",
                    "origin_id": "e4f5c49cfbd92d81df1f078ff0493acff0bc66fc",
                    "request_url": "https://tools.wasabi.atreemo.co.uk/Bink/api/PostMatchedTransaction",
                },
                "timestamp": "2021-10-01 18:52:09",
            },
            "response": {
                "body": {"Error": "Internal Error", "Message": None},
                "status_code": 200,
                "timestamp": "2021-10-01 18:52:09",
            },
        },
    }


@pytest.fixture()
def audit_log_wasabi_success_200():
    return {
        "provider_slug": "wasabi-club",
        "transactions": TRANSACTIONS,
        "audit_data": {
            "request": {
                "body": {
                    "ReceiptNo": "0000A01701000284803",
                    "origin_id": "10e98a2d8845781db23a287f77148b896b521f5a",
                    "request_url": "https://tools.wasabi.atreemo.co.uk/Bink/api/PostMatchedTransaction",
                },
                "timestamp": "2023-01-16 16:37:00",
            },
            "response": {
                "body": {"Error": None, "Message": "Stamp awarded"},
                "status_code": 200,
                "timestamp": "2023-01-16 16:37:03",
            },
        },
    }
