from unittest import mock

import settings
from app.export_transaction import (export_transaction_request_event,
                                    export_transaction_response_event)
from app.message_consumer import MessageConsumer


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


@mock.patch("app.export_transaction.message_queue.add")
def test_export_request(mock_add, audit_log_squaremeal_success_200, dw_request_export):
    export_transaction_request_event(audit_log_squaremeal_success_200)
    mock_add.assert_called_with(
        {
            "event_type": "transaction.exported",
            "event_date_time": "2023-02-07T14:34:19.628925",
            "internal_user_ref": 0,
            "transaction_id": "e2559286-2d84-4256-8a19-d8259e451bac",
            "provider_slug": "squaremeal",
            "transaction_date": "2020-10-27T15:01:59",
            "spend_amount": -8945,
            "spend_currency": "GBP",
            "loyalty_id": "e2559286-2d84-4256-8a19-d8259e451bac",
            "mid": "test-mid-123",
            "scheme_account_id": 0,
            "credentials": "Cl1h4vksFj/8EbTzOORVu+4yMWWS4Yvm1vs7hSzYkRZ0Y/muMuWWKHXohziGiXjOFK9dhI1hW286THYqNKJbDM4cD7fv757wjjadP/wIyYMP8f8JosbitHTSP516Wk+7WpH5TcdmstcPBBYnDCTQOVQYSrVU0FiDiWCr9ZrMcZfaz9XYjh3AzcmJ7pl86cAB",
            "status": "EXPORTED",
            "feed_type": "REFUND",
            "location_id": None,
            "merchant_internal_id": None,
            "payment_card_account_id": 0,
            "settlement_key": "fea4fdbfb49f9e328e57293b420f9dd36a33689f572dd19ff655918c4aeb4515",
            "authorisation_code": "444444",
            "approval_code": "",
            "uid": "e06dbc5f-8ed3-4a49-b830-6f5e65b563ec",
        },
        "squaremeal",
        settings.DW_QUEUE_NAME,
    )


@mock.patch("app.export_transaction.message_queue.add")
def test_export_response_data_in_body(mock_add, audit_log_squaremeal_success_200):
    export_transaction_response_event(audit_log_squaremeal_success_200)
    mock_add.assert_called_with(
        {
            "event_type": "transaction.exported.response",
            "event_date_time": "2023-02-07T14:34:19.628925",
            "transaction_id": "e2559286-2d84-4256-8a19-d8259e451bac",
            "provider_slug": "squaremeal",
            "status_code": 200,
            "response_message": "Bink Transaction details processed sucessfully!",
            "uid": "e06dbc5f-8ed3-4a49-b830-6f5e65b563ec",
        },
        "squaremeal",
        settings.DW_QUEUE_NAME,
    )


@mock.patch("app.export_transaction.message_queue.add")
def test_export_response_wasabi_success(mock_add, audit_log_wasabi_success_200):
    export_transaction_response_event(audit_log_wasabi_success_200)
    mock_add.assert_called_with(
        {
            "event_type": "transaction.exported.response",
            "event_date_time": "2023-02-07T14:34:19.628925",
            "transaction_id": "e2559286-2d84-4256-8a19-d8259e451bac",
            "provider_slug": "wasabi-club",
            "status_code": 200,
            "response_message": "Stamp awarded",
            "uid": "e06dbc5f-8ed3-4a49-b830-6f5e65b563ec",
        },
        "wasabi-club",
        settings.DW_QUEUE_NAME,
    )


@mock.patch("app.export_transaction.message_queue.add")
def test_export_response_wasabi_fail(mock_add, audit_log_wasabi_failure_200):
    export_transaction_response_event(audit_log_wasabi_failure_200)
    mock_add.assert_called_with(
        {
            "event_type": "transaction.exported.response",
            "event_date_time": "2023-02-07T14:34:19.628925",
            "transaction_id": "e2559286-2d84-4256-8a19-d8259e451bac",
            "provider_slug": "wasabi-club",
            "status_code": 200,
            "response_message": "Internal Error",
            "uid": "e06dbc5f-8ed3-4a49-b830-6f5e65b563ec",
        },
        "wasabi-club",
        settings.DW_QUEUE_NAME,
    )


@mock.patch("app.export_transaction.message_queue.add")
def test_bpl_export_success(mock_add, audit_log_viator_success_200):
    export_transaction_response_event(audit_log_viator_success_200)
    mock_add.assert_called_with(
        {
            "event_type": "transaction.exported.response",
            "event_date_time": "2023-02-07T14:34:19.628925",
            "transaction_id": "e2559286-2d84-4256-8a19-d8259e451bac",
            "provider_slug": "bpl-viator",
            "status_code": 200,
            "response_message": "Awarded",
            "uid": "e06dbc5f-8ed3-4a49-b830-6f5e65b563ec",
        },
        "bpl-viator",
        settings.DW_QUEUE_NAME,
    )


@mock.patch("app.export_transaction.message_queue.add")
def test_bpl_export_success(mock_add, audit_log_viator_404_fail):
    export_transaction_response_event(audit_log_viator_404_fail)
    mock_add.assert_called_with(
        {
            "event_type": "transaction.exported.response",
            "event_date_time": "2023-02-07T14:34:19.628925",
            "transaction_id": "e2559286-2d84-4256-8a19-d8259e451bac",
            "provider_slug": "bpl-viator",
            "status_code": 404,
            "response_message": "NO_ACTIVE_CAMPAIGNS",
            "uid": "e06dbc5f-8ed3-4a49-b830-6f5e65b563ec",
        },
        "bpl-viator",
        settings.DW_QUEUE_NAME,
    )
