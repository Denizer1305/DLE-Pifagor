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
# Обращения пользователей

Модуль обращений связывает публичную форму обратной связи, обращения из личных кабинетов и административную обработку заявок.

## Основные сценарии

- отправка обращения из публичной формы;
- отправка обращения из личного кабинета пользователя;
- автоматическое заполнение имени, email, телефона и организации из профиля, если данные доступны;
- прикрепление файлов к обращению;
- отображение вложений у администратора и в email-уведомлении;
- просмотр деталей обращения;
- смена статуса обращения администратором;
- создание уведомления о новом обращении.

## Frontend

- `src/modules/feedback/pages/FeedbackPage.vue` - страница обращения в ЛК.
- `src/modules/feedback/components/FeedbackRequestForm.vue` - форма обращения.
- `src/modules/admin/pages/AdminFeedbackPage.vue` - административный список обращений.
- `src/modules/public/components/contacts/ContactFeedbackSection.vue` - публичная форма контактов.

## Backend

Backend отвечает за хранение обращения, вложений, статусов, отправку email и создание уведомлений для администраторов.

## Ограничения UI

В списках длинный текст обращения должен сокращаться. Полное содержание открывается через детальный просмотр, чтобы карточки не растягивали страницу.

---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
