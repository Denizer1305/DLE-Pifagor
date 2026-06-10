from __future__ import annotations

from uuid import uuid4


def unique_code(prefix: str = "test") -> str:
    """
    Возвращает уникальный технический код.
    """

    return f"{prefix}_{uuid4().hex[:12]}"


def unique_title(prefix: str = "Тест") -> str:
    """
    Возвращает уникальное название.
    """

    return f"{prefix} {uuid4().hex[:8]}"


def unique_email(prefix: str = "testing") -> str:
    """
    Возвращает уникальный email.
    """

    return f"{prefix}_{uuid4().hex[:10]}@example.com"


def extract_results(response_data):
    """
    Возвращает список объектов из paginated/non-paginated/API-wrapped ответа.
    """

    if isinstance(response_data, list):
        return response_data

    if not isinstance(response_data, dict):
        return []

    if "results" in response_data:
        return response_data["results"]

    data = response_data.get("data")

    if isinstance(data, list):
        return data

    if isinstance(data, dict):
        if "results" in data:
            return data["results"]

        if "items" in data:
            return data["items"]

    if "items" in response_data:
        return response_data["items"]

    return []


def get_choice_value(
    model,
    choices_class_name: str,
    *choice_names: str,
    default: str,
) -> str:
    """
    Безопасно достаёт значение choices из вложенного класса модели.
    """

    choices_class = getattr(model, choices_class_name, None)

    if choices_class is None:
        return default

    for choice_name in choice_names:
        if hasattr(choices_class, choice_name):
            return getattr(choices_class, choice_name)

    return default
