from unittest import mock
from unittest.mock import Mock

import pytest

from app.message_consumer import MessageConsumer


@pytest.fixture()
def message_consumer():
    connection = Mock()
    return MessageConsumer(connection=connection)


@pytest.fixture()
def audit_log_viator_success():
    return {
        "provider_slug": "bpl-viator",
        "transactions": [
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
                "encrypted_credentials": "Cl1h4vksFj/8EbTzOORVu+4yMWWS4Yvm1vs7hSzYkRZ0Y/muMuWWKHXohziGiXjOFK9dhI1hW286THYqNKJbDM4cD7fv757wjjadP/wIyYMP8f8JosbitHTSP516Wk+7WpH5TcdmstcPBBYnDCTQOVQYSrVU0FiDiWCr9ZrMcZfaz9XYjh3AzcmJ7pl86cAB",
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
        ],
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


@mock.patch("app.message_consumer.export_transaction_request_event")
@mock.patch("app.message_consumer.export_transaction_response_event")
def test_on_message_exports_request_if_retry_count_0(export_response, export_request, message_consumer):
    body = {"retry_count": 0}
    message_consumer.on_message(body, mock.Mock())
    export_request.assert_called_with(data=body)
    export_response.assert_called_with(data=body)


@mock.patch("app.message_consumer.export_transaction_request_event")
@mock.patch("app.message_consumer.export_transaction_response_event")
def test_on_message_exports_request_if_retry_count_bigger_than_0(export_response, export_request, message_consumer):
    body = {"retry_count": 1}
    MessageConsumer.on_message(body, mock.Mock())
    assert not export_request.called
    export_response.assert_called_with(data=body)
