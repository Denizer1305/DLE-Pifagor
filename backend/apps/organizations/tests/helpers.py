from __future__ import annotations


def get_response_items(response) -> list:
    """
    Возвращает список объектов из обычного или пагинированного ответа.
    """

    data = response.data

    if isinstance(data, list):
        return data

    if not isinstance(data, dict):
        return []

    if "results" in data and isinstance(data["results"], list):
        return data["results"]

    if "items" in data and isinstance(data["items"], list):
        return data["items"]

    nested_data = data.get("data")

    if isinstance(nested_data, list):
        return nested_data

    if isinstance(nested_data, dict):
        if "results" in nested_data and isinstance(nested_data["results"], list):
            return nested_data["results"]

        if "items" in nested_data and isinstance(nested_data["items"], list):
            return nested_data["items"]

    return []


def get_response_total_count(response) -> int:
    """
    Возвращает общее количество объектов из ответа.
    """

    data = response.data

    if isinstance(data, list):
        return len(data)

    if not isinstance(data, dict):
        return 0

    if "count" in data:
        return int(data["count"])

    if "total_count" in data:
        return int(data["total_count"])

    nested_data = data.get("data")

    if isinstance(nested_data, dict):
        if "count" in nested_data:
            return int(nested_data["count"])

        if "total_count" in nested_data:
            return int(nested_data["total_count"])

    return len(get_response_items(response))


def get_error_message(response) -> str:
    """
    Возвращает текст ошибки из стандартного или обёрнутого error-response.
    """

    data = response.data

    if isinstance(data, dict):
        if "error" in data and isinstance(data["error"], dict):
            return str(data["error"].get("message", ""))

        if "detail" in data:
            return str(data["detail"])

        return str(data)

    return str(data)
