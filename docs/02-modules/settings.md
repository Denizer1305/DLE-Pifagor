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
# Настройки пользователя

Модуль настроек отвечает за персонализацию интерфейса, уведомления, приватность, активную роль и безопасность аккаунта.

## Разделы

- `Внешний вид` - режим отображения, цветовая тема, логотип, язык и визуальные параметры.
- `Уведомления` - каналы, типы событий и предпочтения пользователя.
- `Приватность` - видимость контактных и профильных данных.
- `Роли` - активная роль пользователя и доступные рабочие пространства.
- `Безопасность` - сессии, параметры входа и защитные настройки.

## Frontend

- `src/modules/settings/pages/SettingsPage.vue` - центр настроек.
- `src/modules/settings/pages/AppearanceSettingsPage.vue` - внешний вид.
- `src/modules/settings/pages/NotificationSettingsPage.vue` - уведомления.
- `src/modules/settings/pages/PrivacySettingsPage.vue` - приватность.
- `src/modules/settings/pages/RoleSettingsPage.vue` - роли.
- `src/modules/settings/pages/SecuritySettingsPage.vue` - безопасность.

## Темы

Цветовая тема управляет CSS-переменными и логотипом платформы. Темный режим должен применяться только тогда, когда выбран темный режим отображения или системная тема пользователя требует темный вариант.

## Правило архитектуры

Страницы настроек должны оставаться тонкими: текст хранится в `data`, преобразование данных в `mappers`, состояние и действия в `composables`, а компоненты получают готовые props.

---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
