# Аудит backend: DRF-конструкции, перегруженные файлы и дубли

Документ обновлен после повторного просмотра backend. Учитывается текущее состояние проекта после расширения `apps/testing` и прохождения backend-проверок: `ruff`, `black --check`, `isort --check-only`, `pytest`.

## 1. Django/DRF-конструкции, которые стоит унифицировать

| Конструкция | Где проявляется | Риск | Чем заменить |
| --- | --- | --- | --- |
| Ручные `ViewSet` с повторяемыми CRUD-методами | `apps/organizations/views/admin_*_views.py`, часть `apps/testing/views/*/viewset.py` | Повторяется `get_queryset`, serializer selection, service call, response shape | `ServiceBackedViewSet`, `AdminEntityViewSetMixin`, domain-specific mixins |
| Role-based `BasePermission` классы | `apps/users/permissions`, `apps/organizations/permissions`, `apps/testing/permissions`, `apps/course/permissions`, `apps/materials/permissions` | Повторяются active user, role, owner, organization scope и teacher/learner checks | Общие predicates и базовые permission classes |
| Serializer `create`/`update`, вызывающие service | `apps/education/serializers`, `apps/course/serializers`, `apps/materials/serializers` | Тонкая прокладка повторяется в каждом домене | `ServiceModelSerializer` или явные write serializers с общим helper |
| Selectors `get_*_by_id` | `apps/course/selectors`, `apps/education/selectors`, `apps/materials/selectors`, `apps/organizations/selectors`, `apps/testing/selectors/*/detail.py` | Повторяется safe lookup и exception handling | `get_object_or_none`, `get_required_object`, typed selector helpers |
| Service mutations `create_*`, `update_*`, `update_*_by_id` | `apps/course/services`, `apps/education/services`, `apps/materials/services`, `apps/testing/services`, `apps/organizations/services` | Повторяются assignment, validation, `full_clean`, `save(update_fields)` | `update_model_fields`, `save_changed_fields`, status transition helpers |
| Router files по ролям | `apps/course/urls/*`, `apps/materials/urls/*`, `apps/testing/urls/*` | Admin/teacher/learner/public router definitions часто совпадают | `register_role_routes(router, registry)` или shared route registry |
| Test factories | `apps/course/tests/factories.py`, `apps/education/tests/factories.py`, `apps/organizations/tests/factories.py`, `apps/testing/tests/factories/*` | Повторяются users/org/departments/subjects fixtures | Общая factory library + доменные factories |

`ModelViewSet`, `APIView`, `ModelSerializer` и `BasePermission` не являются проблемой сами по себе. Рефакторить стоит только места, где повторяется сценарий, а не просто класс DRF.

## 2. Перегруженные backend-файлы

Миграции не учитываются как проблема: они большие по природе и не являются местом бизнес-логики.

| Приоритет | Файл | Симптом | Что вынести |
| --- | --- | --- | --- |
| Высокий | `apps/users/serializers/admin_user_serializers.py` | Около 720 строк, 13 serializer-классов | `admin_users/serializers/list.py`, `detail.py`, `write.py`, `roles.py`, `status.py` |
| Высокий | `apps/users/views/admin_user_views.py` | Около 731 строки; list/detail/create/update/lifecycle/bulk/status в одном ViewSet | Action mixins + тонкий `AdminUserViewSet` |
| Высокий | `apps/users/services/admin_users/role_services.py` | Около 670 строк, много role lifecycle сценариев | `roles/assign.py`, `revoke.py`, `restore.py`, `queries.py` |
| Высокий | `apps/course/selectors/access_selectors.py` | Около 626 строк, много условий доступа | Разделить на learner/teacher/admin/public selectors |
| Высокий | `apps/materials/selectors/access_selectors.py` | Около 561 строки, похожая проблема доступа | Разделить по ролям и сценариям |
| Высокий | `apps/users/selectors/user_join_request_selectors.py` | Около 561 строки, разные scope и состояния заявок | Разделить по ролям и статусам |
| Высокий | `apps/users/services/admin_users/bulk_services.py` | Около 576 строк, bulk import/validation/apply/reporting | Разнести import, validation, apply, reporting |
| Средний | `apps/users/services/admin_users/update_services.py` | Около 446 строк, user/profile/roles/org relations | Разделить по зонам обновления |
| Средний | `apps/users/services/admin_users/audit_services.py` | Около 460 строк, ручная сборка audit payload | Event builder + typed event helpers |
| Средний | `apps/users/services/admin_users/status_services.py` | Около 443 строки, lifecycle пользователя | `activate`, `deactivate`, `archive`, `restore` |
| Средний | `apps/organizations/services/teacher_subject_services.py` | Около 415 строк, сложные связи teacher/subject/group | Validators + mutation helpers |
| Средний | `apps/notifications/managers/notification_managers.py` | 27 методов, manager стал service/selectors слоем | Business methods в services/selectors |
| Средний | `apps/users/managers/user_manager.py` | Создание разных типов пользователей и child-user flow | Create flows в services |
| Средний | `apps/testing/views/bank/viewset.py` | Около 315 строк, CRUD + filters + actions + duplication/import | Разделить item flow, status actions, import/duplication mixins |

## 3. Перегруженные области по модулям

### `users`

Самый насыщенный backend-модуль. Основные риски:

- `AdminUserViewSet` координирует слишком много сценариев.
- `admin_user_serializers.py` смешивает list/detail/write/status/roles контракты.
- `role_services.py`, `bulk_services.py`, `status_services.py`, `update_services.py` уже выглядят как несколько сервисов внутри одного файла.
- Permissions в `users` содержат много похожих role/object checks.

Целевое направление: вертикально разложить `admin_users` по use cases, а не только по техническим слоям.

### `organizations`

Повторяет frontend-проблему: много однотипных CRUD-сущностей.

Повторяются:

- admin viewsets для organization, department, study group, subject, teacher organization, teacher subject, group curator;
- service-функции create/update;
- selectors `get_*_by_id`, `get_active_*_by_id`;
- permission-классы `CanManage*`.

Целевое направление: `AdminOrganizationEntityViewSetMixin`, общий `OrganizationEntityPermission`, helpers для organization scope.

### `testing`

Модуль стал заметно шире: появились/расширены bank, taking, review, integrity. Это полезный рост, но теперь есть несколько повторяемых семейств.

Зоны внимания:

- `TestViewSet`, `TestQuestionViewSet`, `TestQuestionOptionViewSet`, `TestAttemptViewSet`, `TestAttemptAnswerViewSet`, `QuestionBankItemViewSet`, `QuestionBankOptionViewSet` повторяют ModelViewSet mechanics.
- `TestTakingViewSet` и `TestReviewViewSet` держат action orchestration; они не критично тяжелые, но нуждаются в сохранении тонкого слоя.
- `apps/testing/permissions/*` повторяют teacher/admin/learner scope predicates.
- `apps/testing/selectors/*/detail.py` почти полностью повторяют `get_*_by_id`.
- `apps/testing/services/*/mutations.py` повторяют create/update payload mechanics.
- `apps/testing/urls/admin_urls.py` и `teacher_urls.py` почти идентичны, `learner_urls.py` отличается меньшим набором viewsets.

Целевое направление:

- `TestingModelViewSetMixin` для serializer selection/service calls.
- `TestingRoleScopeMixin` для admin/teacher/learner queryset restrictions.
- Общие `get_testing_object_by_id` helpers.
- Shared router registry для admin/teacher.

### `course` и `materials`

В обоих модулях уже есть хорошая структура `services/selectors/views/permissions`, но повторяются:

- access selectors;
- mutation/status helpers;
- permission base classes;
- admin shared actions;
- factories.

Целевое направление: общий `access` слой по ролям и shared mutation/status helpers.

### `education`

Слой хорошо разложен, но services повторяют lifecycle:

- `create_*`
- `update_*`
- `update_*_by_id`
- `set_current_*_by_id`
- `deactivate_*_by_id`
- `restore_*_by_id`

Целевое направление: `education/services/shared/mutations.py` и `education/services/shared/status.py`.

### `notifications`

`notification_managers.py` содержит много behavior-методов и фактически выполняет роль service/selectors.

Целевое направление: оставить в manager queryset helpers, а бизнес-действия перенести в services/selectors.

## 4. Дубли функциональности

### CRUD viewsets

Основные семьи дублей:

- `apps/organizations/views/admin_*_views.py`
- `apps/testing/views/test/viewset.py`
- `apps/testing/views/question/viewset.py`
- `apps/testing/views/option/viewset.py`
- `apps/testing/views/attempt/viewset.py`
- `apps/testing/views/answer/viewset.py`
- `apps/testing/views/bank/viewset.py`
- `apps/testing/views/bank/option_viewset.py`
- `apps/course/views/*/viewset.py`
- `apps/education/views/*/viewset.py`
- `apps/materials/views/*/viewset.py`

Решение: не один общий ViewSet на весь проект, а по одному base/mixin на домен: `CourseReadWriteViewSetMixin` уже есть, похожий подход нужен для `testing` и `organizations`.

### Service mutations

Повторяются:

- создание объекта из payload;
- применение payload к instance;
- `full_clean`;
- `save`;
- `update_by_id`;
- status transitions.

Файлы:

- `apps/course/services/course*/**`
- `apps/materials/services/**`
- `apps/education/services/*_services.py`
- `apps/testing/services/*/mutations.py`
- `apps/organizations/services/*_services.py`

Решение: маленькие helpers вместо большой универсальной service-фабрики.

### Permissions

Повторяются checks:

- authenticated + active;
- admin/superadmin bypass;
- teacher owns object;
- learner owns attempt/result;
- organization scope;
- read-only vs write.

Решение:

- `is_active_user(user)`
- `has_any_role(user, roles)`
- `is_teacher_owner(user, obj)`
- `is_learner_owner(user, obj)`
- `is_org_admin(user, organization)`
- доменные base permissions поверх этих predicates.

### Selectors

`get_*_by_id` есть почти в каждом домене.

Решение:

```python
def get_object_or_none(queryset, **filters):
    ...

def get_required_object(queryset, **filters):
    ...
```

После этого доменные selectors остаются для оптимизированных queryset и сложного scope, а не для повторяющегося `try/except`.

### URL routers

Повторяются role routers:

- `apps/testing/urls/admin_urls.py`
- `apps/testing/urls/teacher_urls.py`
- `apps/course/urls/*.py`
- `apps/materials/urls/*.py`

Решение: route registry:

```python
ROLE_ROUTES = (
    ("tests", TestViewSet, "testing-tests"),
    ...
)
```

И helper, который добавляет role prefix к basename.

### Test factories

Повторяются:

- `create_user`
- `create_superadmin`
- `create_teacher`
- `create_learner`
- `create_organization`
- `create_department`
- `create_study_group`
- `create_subject`

Решение: общий `tests/factories/common.py` или `apps/core/tests/factories.py`; доменные factories должны создавать только сущности своего модуля.

## 5. Рекомендуемый порядок работ

1. Разбить `apps/users/serializers/admin_user_serializers.py`.
2. Разгрузить `apps/users/views/admin_user_views.py`.
3. Вынести общие permission predicates.
4. Ввести base/mixin для `organizations` admin CRUD.
5. Ввести `TestingModelViewSetMixin` и `TestingRoleScopeMixin`.
6. Унифицировать selectors `get_*_by_id`.
7. Вынести mutation/status helpers.
8. Разнести access selectors в `course` и `materials`.
9. Упростить role routers через registry.
10. Собрать общие test factories.

## 6. Что не абстрагировать слишком рано

- Миграции: размер не является проблемой.
- Уникальные business flows в `testing`: taking, review и integrity не стоит загонять в универсальный CRUD.
- Serializers с разным API-контрактом: лучше разделить файлы, чем делать один универсальный serializer.
- Permissions с разной доменной семантикой: общими должны быть predicates, а не один класс на весь проект.
- Viewsets с action orchestration: лучше держать action тонким и выносить business logic в services, чем прятать все в магический base class.
