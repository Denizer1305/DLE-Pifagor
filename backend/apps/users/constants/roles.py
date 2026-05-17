from django.db import models


class RoleCode(models.TextChoices):
    """
    Системные коды ролей пользователя.

    Коды ролей используются в backend-логике, permissions, services,
    serializers и frontend-маршрутизации.

    Важно:
        В коде роли хранятся на английском языке.
        Для пользователя роли отображаются на русском языке.
    """

    LEARNER = "learner", "Учащийся"
    GUARDIAN = "guardian", "Родитель / законный представитель"
    TEACHER = "teacher", "Преподаватель"
    CURATOR = "curator", "Куратор группы"
    METHODIST = "methodist", "Методист"
    ORGANIZER = "organizer", "Педагог-организатор"
    MENTOR = "mentor", "Педагог-наставник"
    DEPARTMENT_HEAD = "department_head", "Заведующий отделением"
    DIRECTOR = "director", "Директор"
    ORG_ADMIN = "org_admin", "Администратор организации"
    SUPERADMIN = "superadmin", "Суперадминистратор"


LEARNER_ROLE_CODES = {
    RoleCode.LEARNER,
}
"""Роли учащихся."""


GUARDIAN_ROLE_CODES = {
    RoleCode.GUARDIAN,
}
"""Роли родителей и законных представителей."""


STAFF_ROLE_CODES = {
    RoleCode.TEACHER,
    RoleCode.CURATOR,
    RoleCode.METHODIST,
    RoleCode.ORGANIZER,
    RoleCode.MENTOR,
    RoleCode.DEPARTMENT_HEAD,
    RoleCode.DIRECTOR,
    RoleCode.ORG_ADMIN,
}
"""Роли сотрудников образовательной организации."""


ORGANIZATION_ADMIN_ROLE_CODES = {
    RoleCode.DIRECTOR,
    RoleCode.ORG_ADMIN,
    RoleCode.DEPARTMENT_HEAD,
}
"""Роли, которые участвуют в управлении образовательной организацией."""


ORGANIZATION_REVIEWER_ROLE_CODES = {
    RoleCode.CURATOR,
    RoleCode.DEPARTMENT_HEAD,
    RoleCode.DIRECTOR,
    RoleCode.ORG_ADMIN,
}
"""Роли, которые могут рассматривать заявки внутри образовательной организации."""


TEACHER_REVIEWER_ROLE_CODES = {
    RoleCode.DEPARTMENT_HEAD,
    RoleCode.DIRECTOR,
    RoleCode.ORG_ADMIN,
}
"""Роли, которые могут подтверждать преподавателей."""


LEARNER_REVIEWER_ROLE_CODES = {
    RoleCode.CURATOR,
    RoleCode.DEPARTMENT_HEAD,
    RoleCode.ORG_ADMIN,
}
"""Роли, которые могут подтверждать учащихся в группе."""


GUARDIAN_REVIEWER_ROLE_CODES = {
    RoleCode.CURATOR,
    RoleCode.DEPARTMENT_HEAD,
    RoleCode.ORG_ADMIN,
}
"""Роли, которые могут подтверждать связь родителя и учащегося."""


PLATFORM_ADMIN_ROLE_CODES = {
    RoleCode.SUPERADMIN,
}
"""Роли уровня всей платформы."""


ROLE_LABELS = {
    RoleCode.LEARNER: "Учащийся",
    RoleCode.GUARDIAN: "Родитель / законный представитель",
    RoleCode.TEACHER: "Преподаватель",
    RoleCode.CURATOR: "Куратор группы",
    RoleCode.METHODIST: "Методист",
    RoleCode.ORGANIZER: "Педагог-организатор",
    RoleCode.MENTOR: "Педагог-наставник",
    RoleCode.DEPARTMENT_HEAD: "Заведующий отделением",
    RoleCode.DIRECTOR: "Директор",
    RoleCode.ORG_ADMIN: "Администратор организации",
    RoleCode.SUPERADMIN: "Суперадминистратор",
}
"""Словарь русских названий ролей."""


ROLE_SORT_ORDER = {
    RoleCode.SUPERADMIN: 10,
    RoleCode.DIRECTOR: 20,
    RoleCode.ORG_ADMIN: 30,
    RoleCode.DEPARTMENT_HEAD: 40,
    RoleCode.METHODIST: 50,
    RoleCode.CURATOR: 60,
    RoleCode.TEACHER: 70,
    RoleCode.ORGANIZER: 80,
    RoleCode.MENTOR: 90,
    RoleCode.GUARDIAN: 100,
    RoleCode.LEARNER: 110,
}
"""Порядок отображения ролей в интерфейсе и админке."""
