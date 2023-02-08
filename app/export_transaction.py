import typing as t

import dateutil.parser as parser

import settings
from app import message_queue


class ExportedTransactionRequest(t.TypedDict):
    event_type: str
    event_date_time: str
    internal_user_ref: str
    transaction_id: str
    provider_slug: str
    transaction_date: str
    spend_amount: int
    spend_currency: str
    loyalty_id: str
    mid: str
    scheme_account_id: int
    credentials: str
    status: str
    feed_type: t.Optional[str]
    location_id: t.Optional[str]
    merchant_internal_id: t.Optional[int]
    payment_card_account_id: t.Optional[str]
    settlement_key: t.Optional[str]
    authorisation_code: t.Optional[str]
    approval_code: t.Optional[str]
    uid: str


class ExportedTransactionResponse(t.TypedDict):
    event_type: str
    event_date_time: str
    transaction_id: str
    provider_slug: str
    status_code: str
    response_message: dict
    uid: str


def export_transaction_request_event(data: dict) -> None:
    transactions = data["transactions"]
    provider_slug = data["provider_slug"]
    for transaction in transactions:
        transaction_datetime = parser.parse(transaction["transaction_date"])
        exported_transaction_request = ExportedTransactionRequest(
            event_type="transaction.exported",
            event_date_time=transaction["event_date_time"],
            internal_user_ref=transaction["user_id"],
            transaction_id=transaction["transaction_id"],
            provider_slug=provider_slug,
            transaction_date=transaction_datetime.isoformat(),
            spend_amount=transaction["spend_amount"],
            spend_currency=transaction["spend_currency"],
            loyalty_id=transaction["loyalty_id"],
            mid=transaction["mid"],
            scheme_account_id=transaction["scheme_account_id"],
            credentials=transaction["encrypted_credentials"],
            status=transaction["status"],
            feed_type=transaction["feed_type"],
            location_id=transaction["location_id"],
            merchant_internal_id=transaction["merchant_internal_id"],
            payment_card_account_id=transaction["payment_card_account_id"],
            settlement_key=transaction["settlement_key"],
            authorisation_code=transaction["authorisation_code"],
            approval_code=transaction["approval_code"],
            uid=transaction["export_uid"],
        )
        message_queue.add(exported_transaction_request, provider_slug, settings.DW_QUEUE_NAME)


def export_transaction_response_event(data: dict) -> None:
    transactions = data["transactions"]
    response = data["audit_data"]["response"]
    provider_slug = data["provider_slug"]
    status_code = response["status_code"]
    response_body = response["body"]

    for transaction in transactions:
        if "bpl" in provider_slug:
            try:
                response_body = response_body["code"]
            except (AttributeError, TypeError):
                response_body = response_body
        elif (
            "wasabi" in provider_slug
            and "Error" in response_body.keys()
            or "wasabi" in provider_slug
            and "Message" in response_body.keys()
        ):
            response_body = response_body.get("Error") if response_body.get("Error") else response_body.get("Message")

        exported_transaction_response = ExportedTransactionResponse(
            event_type="transaction.exported.response",
            event_date_time=transaction["event_date_time"],
            transaction_id=transaction["transaction_id"],
            provider_slug=provider_slug,
            status_code=status_code,
            response_message=response_body,
            uid=transaction["export_uid"],
        )
        message_queue.add(exported_transaction_response, provider_slug, settings.DW_QUEUE_NAME)
