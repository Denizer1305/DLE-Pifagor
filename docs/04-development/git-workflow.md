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
# Git Workflow

## Основные ветки

- `main` — стабильная версия проекта;
- `develop` — основная ветка разработки;
- `feature/*` — новые функции;
- `fix/*` — исправления ошибок;
- `docs/*` — документация.

---

## Процесс работы

1. Создать ветку от `develop`.
2. Выполнить задачу.
3. Проверить проект локально.
4. Написать или обновить тесты.
5. Обновить документацию при необходимости.
6. Сделать pull request в `develop`.
7. После проверки слить.
8. Для релиза слить `develop` в `main`.

---

## Пример

```bash
git checkout develop
git pull
git checkout -b feature/assignments-review
```

После работы:

```bash
git add .
git commit -m "feat(assignments): add submission review panel"
git push origin feature/assignments-review
```

---

## Релизы

```bash
git tag v1.1.0
git push origin v1.1.0
```

---

## Главный принцип

> Стабильная ветка всегда должна запускаться.

---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
