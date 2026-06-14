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
# Release checklist

## Перед релизом

- [ ] backend system check проходит;
- [ ] миграции созданы и проверены;
- [ ] ruff проходит;
- [ ] black/isort проходят;
- [ ] frontend type-check проходит;
- [ ] frontend build проходит;
- [ ] документация обновлена;
- [ ] README и changelog актуальны;
- [ ] env-переменные описаны;
- [ ] секреты не попали в git;
- [ ] ключевые пользовательские сценарии проверены вручную.

## Проверка UI

- [ ] публичные страницы;
- [ ] auth страницы;
- [ ] ЛК администратора;
- [ ] ЛК преподавателя;
- [ ] ЛК студента;
- [ ] ЛК родителя;
- [ ] профиль;
- [ ] настройки;
- [ ] календарь и заметки;
- [ ] уведомления;
- [ ] обращения;
- [ ] организации.

## После релиза

- [ ] проверить логи backend;
- [ ] проверить ошибки frontend;
- [ ] проверить отправку email и уведомлений;
- [ ] проверить backup-процедуры.

---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
