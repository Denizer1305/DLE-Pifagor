# Troubleshooting

## 401 Unauthorized

Проверьте:

- access token передается в запросе;
- refresh token существует и не истек;
- endpoint refresh доступен;
- frontend не делает защищенные запросы до восстановления сессии.

## 403 Forbidden

Проверьте:

- роль пользователя;
- активную роль;
- permissions endpoint;
- наличие пользователя в нужной группе или организации.

## Данные dashboard не отображаются

Проверьте:

- backend endpoint возвращает данные для текущей роли;
- mapper поддерживает фактический формат DTO;
- frontend не подменяет реальные данные тестовыми;
- empty state показывается только при пустом ответе.

## Ошибки форматирования backend

Запустите:

```sh
cd backend
.venv/bin/python -m ruff check apps config
.venv/bin/python -m black apps config
.venv/bin/python -m isort --profile black apps config
```

## Ошибки frontend type-check

Проверьте обязательные поля типов, импорты и соответствие props общим компонентам.
