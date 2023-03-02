def _get_bpl_response(response_body: dict) -> str | dict:
    try:
        return response_body["code"]
    except (KeyError, TypeError):
        return response_body


def _get_wasabi_response(response_body: dict) -> str | dict:
    try:
        return response_body["Error"] if response_body.get("Error") else response_body["Message"]
    except (KeyError, TypeError):
        return response_body


RESPONSE_METHODS = {"bpl": _get_bpl_response, "wasabi-club": _get_wasabi_response}


def get_response_body(scheme_slug: str, response_body: dict | str) -> dict | str:
    if "bpl" in scheme_slug:
        scheme_slug = "bpl"

    if scheme_slug in RESPONSE_METHODS.keys():
        response_body = RESPONSE_METHODS[scheme_slug](response_body)  # type: ignore
    return response_body
