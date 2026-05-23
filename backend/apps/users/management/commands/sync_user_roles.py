from __future__ import annotations

from apps.users.models import Role
from django.core.management.base import BaseCommand


class Command(BaseCommand):
    """
    Синхронизирует системные роли пользователей.

    Команда создаёт или обновляет записи справочника users_role
    на основе RoleCode, ROLE_LABELS и ROLE_SORT_ORDER.

    Пример:
        python manage.py sync_user_roles
    """

    help = "Создаёт или обновляет системные роли пользователей."

    def handle(self, *args, **options):
        """
        Выполняет синхронизацию системных ролей.

        Args:
            *args:
                Позиционные аргументы команды.
            **options:
                Опции команды.
        """

        roles = Role.objects.ensure_system_roles()

        self.stdout.write(
            self.style.SUCCESS(f"Системные роли синхронизированы: {len(roles)}.")
        )

        for role in roles:
            self.stdout.write(f"- {role.code}: {role.label}")
