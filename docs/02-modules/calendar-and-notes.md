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
# Календарь и заметки

Модуль календаря и заметок помогает пользователю вести личный план на день, создавать события, хранить заметки и видеть ближайшие задачи на главной странице личного кабинета.

## Основные сценарии

- просмотр календаря в личном кабинете и на отдельной странице;
- создание события на выбранную дату;
- выбор темы события для более точной классификации;
- создание личной заметки;
- отображение заметок на календаре;
- просмотр длинной заметки в модальном окне;
- удаление события или заметки с синхронным исчезновением из календаря и панелей.

## Frontend

- `src/modules/calendar/pages/CalendarPage.vue` - полноценная страница календаря.
- `src/modules/notes/pages/NotesPage.vue` - список личных заметок пользователя.
- `src/components/dashboard/panels/DashboardCalendar.vue` - компактный календарь на главной странице ЛК.
- `src/components/dashboard/panels/DashboardNotesPanel.vue` - панель заметок.

## Интеграции

Календарь и заметки связаны с модулем уведомлений: событие или заметка могут создавать уведомление, а удаление сущности должно убирать связанные отображения.

## Правило отображения

Короткие элементы показываются прямо в карточках и календаре. Длинный текст должен сокращаться, а полный просмотр открываться через модальное окно.

---
<!-- DLE-Pifagor Documentation Footer -->
<p align="center">
  <sub>DLE-Pifagor · единая цифровая образовательная среда</sub><br />
  <sub><a href="../../docs/README.md">К индексу документации</a> · <a href="../../README.md">К README проекта</a></sub>
</p>
<!-- /DLE-Pifagor Documentation Footer -->
