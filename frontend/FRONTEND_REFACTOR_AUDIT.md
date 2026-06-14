# Аудит frontend: нативные элементы, перегруженные файлы и дубли

Документ обновлен после повторного просмотра проекта. Он фиксирует текущие зоны риска во `frontend`: нативные элементы, которые стоит обернуть в единые компоненты, перегруженные страницы и компоненты, а также устойчивые дубли функциональности.

## 1. Нативные элементы

Повторная проверка Vue-файлов показала:

| Элемент | Количество | Комментарий |
| --- | ---: | --- |
| `input` | 116 | Основная масса форм. Нужны единые обертки для label/error/help/loading states. |
| `textarea` | 19 | Встречается в feedback, dashboard, organizations, admin forms. |
| `input[type="checkbox"]` | 19 | Согласия, настройки, фильтры и флаги сущностей. |
| `input[type="date"]` | 10 | Admin/user/profile/calendar/organization формы. |
| `table` | 9 | Admin users и почти все organization list tables. |
| `input[type="file"]` | 3 | Feedback attachments, avatar upload, public contact attachments. |
| `input[type="range"]` | 3 | Crop modal. |
| `input[type="radio"]` | 1 | Register role switcher. |
| `input[type="time"]` | 1 | Notification settings. |
| `select`, `dialog`, `details`, `summary`, `progress`, `meter` | 0 | Массовой проблемы нет. Переключатель языка уже кастомный. |

### Что заменить в первую очередь

| Элемент | Где заметнее всего | Почему | Чем заменить |
| --- | --- | --- | --- |
| `table` | `AdminUsersWorkspace`, `DepartmentListTable`, `StudyGroupListTable`, `SubjectListTable`, `TeacherOrganizationListTable`, `TeacherSubjectListTable`, `GroupCuratorListTable`, `JoinRequestListTable`, `OrganizationListTable` | Повторяются empty/loading states, actions, responsive-поведение и структура строк | `BaseDataTable` или `OrganizationEntityTable` |
| `input[type="file"]` | `FeedbackRequestForm`, `ProfileEditAvatarCard`, `ContactFeedbackMessageFields` | Нативный вид плохо контролируется и плохо согласуется с дизайн-системой | `BaseFileUpload` с drag-and-drop, списком файлов и ошибками |
| `input[type="date"]`, `input[type="time"]` | Формы пользователя, календарь, настройки уведомлений, organization forms | Нативные picker'ы по-разному выглядят между браузерами | `BaseDatePicker`, `BaseTimePicker` |
| `input[type="range"]` | `ProfileAvatarCropModal` | Нужен единый slider с понятным значением и клавиатурным управлением | `BaseSlider` |
| `input[type="checkbox"]` | Auth agreement, settings, filters, organization flags | Повторяются label/error/disabled состояния | `BaseCheckbox`, `BaseToggle` |
| `textarea` | Feedback, dashboard create modal, organization/admin forms | Нужны autosize, counter, error/hint и единая стилизация | `BaseTextarea` |

### Что можно оставить нативным

Обычные текстовые `input` можно оставить нативными внутри `BaseInput`. Важно унифицировать не сам HTML-тег, а контракт: `label`, `hint`, `error`, `disabled`, `loading`, `required`, `autocomplete`, `aria-*`.

## 2. Перегруженные страницы

Повторный расчет сложности подтвердил, что самые тяжелые страницы находятся в `organizations`.

| Приоритет | Файл | Текущий симптом | Что вынести |
| --- | --- | --- | --- |
| Высокий | `src/modules/organizations/pages/OrganizationsPage.vue` | Самая тяжелая страница: список, фильтры, детали, форма, код организации, actions | `useOrganizationsPage`, `useOrganizationCodeModal`, общий CRUD controller |
| Высокий | `src/modules/organizations/pages/StudyGroupsPage.vue` | CRUD, details, code modal, table actions и form orchestration | `useStudyGroupsPage`, общий code modal controller |
| Высокий | `src/modules/organizations/pages/DepartmentsPage.vue` | CRUD, фильтры, details modal, table actions | `useDepartmentsPage`, общий entity controller |
| Высокий | `src/modules/organizations/pages/SubjectsPage.vue` | Повторяет CRUD-паттерн departments/study groups | `useSubjectsPage` |
| Высокий | `src/modules/organizations/pages/GroupCuratorsPage.vue` | Повторяет CRUD-паттерн teacher entities | `useGroupCuratorsPage` |
| Высокий | `src/modules/organizations/pages/TeacherOrganizationsPage.vue` | Почти такой же сценарий, как teacher subjects | Общий teacher entity page controller |
| Высокий | `src/modules/organizations/pages/TeacherSubjectsPage.vue` | Почти такой же сценарий, как teacher organizations | Общий teacher entity page controller |
| Средний | `src/modules/settings/pages/AppearanceSettingsPage.vue` | Много UI-состояний и computed для настроек внешнего вида | `useAppearanceSettings`, отдельные секции |
| Средний | `src/modules/organizations/pages/JoinRequestsPage.vue` | Таблица, детали и review flow на одной странице | `useJoinRequestsPage`, review modal controller |
| Средний | `src/modules/profile/pages/ProfileAchievementsPage.vue` | Фильтры, вычисления, списки и presentation logic | `useProfileAchievements` |

Тонкими остаются public/auth pages: они в основном подключают секции и формы. Их структурное сходство есть, но это допустимый wrapper-дубль.

## 3. Перегруженные компоненты

### Высокий приоритет

| Компонент | Симптом | Рекомендация |
| --- | --- | --- |
| `src/modules/organizations/components/study-groups/StudyGroupForm.vue` | Самый тяжелый компонент по суммарной сложности: большой template и локальные обработчики | Вынести `FormShell`, `FormSection`, reusable field rows |
| `src/components/base/BaseSelect.vue` | Keyboard navigation, dropdown state, positioning, options, outside click | Вынести `useDropdownNavigation` и `useFloatingListbox` |
| `src/modules/profile/components/ProfileAvatarCropModal.vue` | Crop-state, range controls, image processing, watchers | Вынести crop engine в composable, оставить UI тонким |
| `src/modules/public/components/teachers/TeachersOrganizationFilter.vue` | Dropdown/filter state, responsive-поведение, watchers | `useTeacherOrganizationFilter` |
| `src/modules/organizations/components/teacher-organizations/TeacherOrganizationForm.vue` | Повторяет тяжелую структуру organization forms | Общий organization/teacher form shell |
| `src/modules/organizations/components/group-curators/GroupCuratorForm.vue` | Большая форма с тем же pattern | Общие form primitives |
| `src/modules/organizations/components/organizations/OrganizationForm.vue` | Много разметки формы и повторных состояний | `FormSection`, `FormActions`, field wrappers |

### Средний приоритет

| Компонент | Симптом | Рекомендация |
| --- | --- | --- |
| `src/components/dashboard/panels/DashboardCreateItemModal.vue` | Форма, textarea/date/checkbox, submit state внутри модалки | `useDashboardCreateItemForm` |
| `src/modules/admin/components/AdminFeedbackWorkspace.vue` | Фильтры, список, state и details в одном компоненте | Разделить на `FeedbackFilters`, `FeedbackList`, `FeedbackDetails` |
| `src/modules/organizations/components/teacher-subjects/TeacherSubjectForm.vue` | Повтор teacher form pattern | Общий teacher entity form shell |
| `src/components/dashboard/panels/DashboardNotesPanel.vue` | List + editor + локальные actions | `DashboardNotesList` и `DashboardNoteEditor` |
| `src/components/dashboard/layout/DashboardPageScaffold.vue` | Layout state и responsive-control | `useDashboardLayoutState` |
| `src/modules/organizations/components/departments/DepartmentForm.vue` | Повтор organization form pattern | Общий form shell |
| `src/modules/public/components/layout/PublicHeader.vue` | Header state, actions, mobile behavior | Состояние меню вынести в composable |
| `src/modules/public/components/layout/PublicLanguageToggle.vue` | Кастомный dropdown стал лучше UX, но содержит state/listbox behavior | Позже переиспользовать общий dropdown primitive |

## 4. Дубли функциональности

### Organizations CRUD pages

Повторяются функции и сценарии:

- `openCreateForm`
- `openEditForm`
- `closeFormModal`
- `submitForm`
- `selectAndWaitDetails`
- `handleTableAction`
- `updateFormModel`

Файлы:

- `src/modules/organizations/pages/DepartmentsPage.vue`
- `src/modules/organizations/pages/StudyGroupsPage.vue`
- `src/modules/organizations/pages/SubjectsPage.vue`
- `src/modules/organizations/pages/GroupCuratorsPage.vue`
- `src/modules/organizations/pages/TeacherOrganizationsPage.vue`
- `src/modules/organizations/pages/TeacherSubjectsPage.vue`
- частично `src/modules/organizations/pages/OrganizationsPage.vue`

Решение: `useOrganizationEntityCrud` или `createEntityPageController` с параметрами `load`, `create`, `update`, `remove`, `getById`, `initialForm`, `mapFormToPayload`, `mapEntityToForm`.

### Organizations tables

Похожи:

- `DepartmentListTable.vue`
- `StudyGroupListTable.vue`
- `SubjectListTable.vue`
- `GroupCuratorListTable.vue`
- `TeacherOrganizationListTable.vue`
- `TeacherSubjectListTable.vue`
- частично `OrganizationListTable.vue`
- частично `JoinRequestListTable.vue`

Решение: `OrganizationEntityTable` поверх `BaseDataTable`, где domain-specific остаются только columns и action slots.

### Organizations details panels

Структурно почти одинаковые:

- `DepartmentDetailsPanel.vue`
- `GroupCuratorDetailsPanel.vue`
- `StudyGroupDetailsPanel.vue`
- `SubjectDetailsPanel.vue`
- `TeacherOrganizationDetailsPanel.vue`
- `TeacherSubjectDetailsPanel.vue`

Решение: `EntityDetailsPanel` с массивом секций/полей, badge slots и action slots.

### Public sections

Hero/CTA секции похожи по роли:

- `HomeHeroSection.vue`
- `AboutHeroSection.vue`
- `ContactHeroSection.vue`
- `TeachersHeroSection.vue`
- `HomeCtaSection.vue`
- `AboutCtaSection.vue`
- `ContactCtaSection.vue`
- `TeachersCtaSection.vue`

Уже есть `PublicCtaSection.vue`; стоит довести до единого использования. Для hero лучше ввести `PublicHeroSection`, но оставить возможность вариантной композиции.

### Auth pages

`LoginPage`, `RegisterPage`, `ForgotPasswordPage`, `ResetPasswordPage`, `VerifyEmailPage`, `TeacherOrganizationCodePage` почти идентичны как wrappers. Это не критичный дубль: страницы тонкие.

### Admin role pages

`AdminParentsPage`, `AdminStudentsPage`, `AdminTeachersPage` структурно совпадают.

Решение: один `AdminUsersPage` с role из route meta/props.

### Dashboard cards

`DashboardActivityCard.vue` и `DashboardAttentionCard.vue` структурно идентичны.

Решение: `DashboardSectionCard` с visual variant.

## 5. Рекомендуемый порядок работ

1. Вынести `useOrganizationEntityCrud` для pages в `organizations`.
2. Собрать `BaseDataTable`/`OrganizationEntityTable`.
3. Собрать `EntityDetailsPanel`.
4. Объединить `OrganizationCodeModal` и `StudyGroupCodeModal`.
5. Разгрузить organization forms через form primitives.
6. Ввести `BaseTextarea`, `BaseCheckbox`, `BaseDatePicker`, `BaseFileUpload`.
7. Вынести behavior dropdown/listbox из `BaseSelect` и `PublicLanguageToggle`.
8. Перевести public CTA на `PublicCtaSection`.
9. Унифицировать admin role pages.
10. Разобрать тяжелые interactive components: `ProfileAvatarCropModal`, `TeachersOrganizationFilter`, `DashboardCreateItemModal`.

## 6. Что не абстрагировать слишком рано

- Доменные поля форм: пусть остаются явно читаемыми, выносить стоит оболочки и повторяемые states.
- Public content: данные лучше держать рядом с доменной секцией, если смысл секций разный.
- Auth pages: wrapper-дубли не требуют срочного рефакторинга.
- Dashboard pages: общие карточки уже частично вынесены, объединять нужно только реально идентичные компоненты.
