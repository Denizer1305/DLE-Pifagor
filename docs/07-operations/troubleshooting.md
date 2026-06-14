<!-- DLE-Pifagor Documentation Header -->
<p align="center">
  <a href="../../README.md"><img src="../../design/logos/main/pifagor-logo-primary.svg" alt="DLE-Pifagor" width="96" /></a>
</p>

<p align="center">
  <a href="../../docs/README.md">Документация</a> ·
  <a href="../../docs/README.en.md">English version</a> ·
  <a href="../../README.md">README проекта</a>
</p>

---
<!-- /DLE-Pifagor Documentation Header -->
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

---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
