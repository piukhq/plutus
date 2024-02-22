from unittest import mock

from app.export_transaction import export_transaction_request_event, export_transaction_response_event
from app.response_helper import _get_itsu_response


@mock.patch("app.export_transaction.redis")
@mock.patch("app.export_transaction.message_queue.add")
def test_export_request(mock_add, redis_mock, audit_log_squaremeal_success_200, connection_mock):
    redis_mock.exists.return_value = False
    export_transaction_request_event(audit_log_squaremeal_success_200, connection=connection_mock)
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
            "credentials": "Cl1h4vksFj/8EbTzOORVu+4yMWWS4Yvm1vs7hSzYkRZ0Y/muMuWWKHXohziGiXjOFK9dhI1hW286THYqNKJb",
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
        connection_mock,
    )


@mock.patch("app.export_transaction.redis")
@mock.patch("app.export_transaction.message_queue.add")
def test_export_request_record_exists_in_redis(mock_add, redis_mock, audit_log_squaremeal_success_200, connection_mock):
    redis_mock.exists.return_value = True
    export_transaction_request_event(audit_log_squaremeal_success_200, connection=connection_mock)
    mock_add.assert_not_called


@mock.patch("app.export_transaction.message_queue.add")
def test_export_response_data_in_body(mock_add, audit_log_squaremeal_success_200, connection_mock):
    export_transaction_response_event(audit_log_squaremeal_success_200, connection=connection_mock)
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
        connection_mock,
    )


@mock.patch("app.export_transaction.message_queue.add")
def test_export_response_wasabi_success(mock_add, audit_log_wasabi_success_200, connection_mock):
    export_transaction_response_event(audit_log_wasabi_success_200, connection=connection_mock)
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
        connection_mock,
    )


@mock.patch("app.export_transaction.message_queue.add")
def test_export_response_wasabi_fail(mock_add, connection_mock, audit_log_wasabi_failure_200):
    export_transaction_response_event(audit_log_wasabi_failure_200, connection=connection_mock)
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
        connection_mock,
    )


@mock.patch("app.export_transaction.message_queue.add")
def test_bpl_export_success(mock_add, audit_log_viator_success_200, connection_mock):
    export_transaction_response_event(audit_log_viator_success_200, connection=connection_mock)
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
        connection_mock,
    )


@mock.patch("app.export_transaction.message_queue.add")
def test_bpl_export_fail(mock_add, audit_log_viator_404_fail, connection_mock):
    export_transaction_response_event(audit_log_viator_404_fail, connection=connection_mock)
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
        connection_mock,
    )


@mock.patch("app.export_transaction.message_queue.add")
def test_tgi_fridays_export_success(mock_add, audit_log_tgi_fridays_success, connection_mock):
    export_transaction_response_event(audit_log_tgi_fridays_success, connection=connection_mock)
    mock_add.assert_called_with(
        {
            "event_type": "transaction.exported.response",
            "event_date_time": "2024-02-21T16:44:01.320042",
            "transaction_id": "db0b14a3-0ca8-4281-9a77-57b5b88ec0a4",
            "provider_slug": "tgi-fridays",
            "status_code": 201,
            "response_message": {},
            "uid": "1515c96c-7cac-49a8-b09a-521a24c92890",
        },
        connection_mock,
    )


@mock.patch("app.export_transaction.message_queue.add")
def test_tgi_fridays_export_fail(mock_add, audit_log_tgi_fridays_failure_404, connection_mock):
    export_transaction_response_event(audit_log_tgi_fridays_failure_404, connection=connection_mock)
    mock_add.assert_called_with(
        {
            "event_type": "transaction.exported.response",
            "event_date_time": "2024-02-21T16:54:47.799261",
            "transaction_id": "db0b14a3-0ca8-4281-9a77-57b5b88ec0a4",
            "provider_slug": "tgi-fridays",
            "status_code": 404,
            "response_message": "Cannot find corresponding user with ID: 62779001",
            "uid": "dcbe01d8-3a4e-4b9c-8d23-26d78c97b267",
        },
        connection_mock,
    )


def test_get_itsu_response_success():
    body = {
        "ResponseStatus": True,
        "Errors": [],
    }

    assert _get_itsu_response(body) is True


def test_get_itsu_response_errors():
    body = {"ResponseStatus": False, "Errors": [{"ErrorCode": 20, "ErrorDescription": "Invalid location ID (SiteID)"}]}

    assert _get_itsu_response(body) == "Invalid location ID (SiteID)"


def test_get_itsu_response_multiple_errors():
    body = {
        "ResponseStatus": False,
        "Errors": [
            {"ErrorCode": 20, "ErrorDescription": "First error"},
            {"ErrorCode": 21, "ErrorDescription": "Second error"},
        ],
    }

    assert _get_itsu_response(body) == "First error Second error"
