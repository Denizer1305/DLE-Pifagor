from __future__ import annotations

from django.db import migrations

ROLE_DATA = [
    {
        "code": "superadmin",
        "label": "Суперадминистратор",
        "sort_order": 10,
    },
    {
        "code": "director",
        "label": "Директор",
        "sort_order": 20,
    },
    {
        "code": "org_admin",
        "label": "Администратор организации",
        "sort_order": 30,
    },
    {
        "code": "department_head",
        "label": "Заведующий отделением",
        "sort_order": 40,
    },
    {
        "code": "methodist",
        "label": "Методист",
        "sort_order": 50,
    },
    {
        "code": "curator",
        "label": "Куратор группы",
        "sort_order": 60,
    },
    {
        "code": "teacher",
        "label": "Преподаватель",
        "sort_order": 70,
    },
    {
        "code": "organizer",
        "label": "Педагог-организатор",
        "sort_order": 80,
    },
    {
        "code": "mentor",
        "label": "Педагог-наставник",
        "sort_order": 90,
    },
    {
        "code": "guardian",
        "label": "Родитель / законный представитель",
        "sort_order": 100,
    },
    {
        "code": "learner",
        "label": "Учащийся",
        "sort_order": 110,
    },
]


def seed_system_roles(apps, schema_editor):
    """
    Создаёт или обновляет системные роли пользователей.

    Args:
        apps:
            Реестр моделей Django на момент миграции.
        schema_editor:
            Объект управления схемой БД.
    """

    Role = apps.get_model("users", "Role")

    for role_data in ROLE_DATA:
        Role.objects.update_or_create(
            code=role_data["code"],
            defaults={
                "label": role_data["label"],
                "description": "",
                "is_system": True,
                "is_active": True,
                "sort_order": role_data["sort_order"],
            },
        )


def unseed_system_roles(apps, schema_editor):
    """
    Откатывает системные роли.

    Мы не удаляем роли, если они уже используются пользователями.
    Поэтому при откате только отключаем системные роли.

    Args:
        apps:
            Реестр моделей Django на момент миграции.
        schema_editor:
            Объект управления схемой БД.
    """

    Role = apps.get_model("users", "Role")

    Role.objects.filter(
        code__in=[role["code"] for role in ROLE_DATA],
        is_system=True,
    ).update(
        is_active=False,
    )


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(
            seed_system_roles,
            reverse_code=unseed_system_roles,
        ),
    ]
