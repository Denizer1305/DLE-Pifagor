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
