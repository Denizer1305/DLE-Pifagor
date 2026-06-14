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
# Уведомления

Модуль уведомлений отвечает за события платформы, счетчик непрочитанных сообщений, выпадающий список в topbar и отдельную страницу уведомлений.

## Основные сценарии

- загрузка уведомлений пользователя после входа;
- отображение счетчика непрочитанных уведомлений;
- просмотр уведомлений в dropdown;
- переход к связанной сущности, например обращению;
- пометка уведомления прочитанным при открытии;
- скрытие прочитанных уведомлений из списка активных;
- настройка каналов и типов уведомлений на странице настроек.

## Frontend

- `src/modules/notifications/pages/NotificationsPage.vue` - страница уведомлений.
- `src/modules/notifications/components/NotificationBell.vue` - кнопка уведомлений в topbar.
- `src/modules/notifications/components/NotificationDropdown.vue` - выпадающий список.
- `src/modules/notifications/stores/notifications.store.ts` - состояние уведомлений.
- `src/modules/settings/pages/NotificationSettingsPage.vue` - настройки уведомлений.

## Backend

Backend хранит уведомления, пользовательские предпочтения и связи уведомлений с объектами платформы. При создании обращения, события календаря или другой важной сущности backend может создавать уведомление для нужных получателей.

## UI-правило

Пустой список должен показывать спокойное empty-state сообщение. Если уведомления есть, пользователь должен видеть количество и понятное действие: открыть, перейти к сущности или отметить прочитанным.

---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
