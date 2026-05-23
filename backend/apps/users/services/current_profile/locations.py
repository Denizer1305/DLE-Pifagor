from __future__ import annotations

import json
from urllib import error, request

from django.conf import settings


def suggest_cities(*, query: str) -> list[dict[str, str]]:
    normalized_query = query.strip()
    token = getattr(settings, "DADATA_API_TOKEN", "")

    if len(normalized_query) < 2 or not token:
        return []

    payload = json.dumps(
        {
            "query": normalized_query,
            "count": 8,
            "from_bound": {"value": "city"},
            "to_bound": {"value": "city"},
        }
    ).encode("utf-8")
    api_request = request.Request(
        getattr(
            settings,
            "DADATA_SUGGESTIONS_URL",
            "https://suggestions.dadata.ru/suggestions/api/4_1/rs/suggest/address",
        ),
        data=payload,
        headers={
            "Authorization": f"Token {token}",
            "Content-Type": "application/json",
            "Accept": "application/json",
        },
        method="POST",
    )

    try:
        with request.urlopen(api_request, timeout=4) as response:
            response_payload = json.loads(response.read().decode("utf-8"))
    except (error.HTTPError, error.URLError, TimeoutError, json.JSONDecodeError):
        return []

    return [
        {
            "value": suggestion.get("value", ""),
            "unrestricted_value": suggestion.get("unrestricted_value", ""),
        }
        for suggestion in response_payload.get("suggestions", [])
        if suggestion.get("value")
    ]
