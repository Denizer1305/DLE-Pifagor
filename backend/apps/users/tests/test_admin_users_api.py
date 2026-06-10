from __future__ import annotations

from datetime import timedelta
from unittest.mock import patch
from zoneinfo import ZoneInfo

from apps.users.constants.audit import UserAuditAction
from apps.users.constants.lifecycle import UserRoleStatus, UserStatus
from apps.users.constants.roles import RoleCode
from apps.users.models import Role, User, UserAuditLog, UserRole
from django.urls import reverse
from django.utils import timezone
from rest_framework import status
from rest_framework.test import APITestCase


class AdminUsersApiTestCase(APITestCase):
    """
    Тесты API административного управления пользователями.

    Проверяет:
        - доступ к списку пользователей;
        - детальную карточку пользователя;
        - редактирование пользователя;
        - optimistic locking;
        - блокировку и восстановление;
        - архивацию;
        - soft delete;
        - смену ролей;
        - массовые действия;
        - запрет доступа обычному пользователю.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Подготавливает пользователей и роли для тестов.
        """

        cls.superadmin_role = cls.get_or_create_role(
            code=RoleCode.SUPERADMIN,
            label="Суперадминистратор",
            description="Полный доступ к платформе.",
            is_system=True,
            is_active=True,
            sort_order=10,
        )
        cls.learner_role = cls.get_or_create_role(
            code=RoleCode.LEARNER,
            label="Студент",
            description="Пользователь с ролью студента.",
            is_system=True,
            is_active=True,
            sort_order=100,
        )
        cls.teacher_role = cls.get_or_create_role(
            code=RoleCode.TEACHER,
            label="Преподаватель",
            description="Пользователь с ролью преподавателя.",
            is_system=True,
            is_active=True,
            sort_order=90,
        )
        cls.guardian_role = cls.get_or_create_role(
            code=RoleCode.GUARDIAN,
            label="Родитель",
            description="Пользователь с ролью родителя.",
            is_system=True,
            is_active=True,
            sort_order=110,
        )

        cls.superadmin = cls.create_user(
            email="superadmin@example.com",
            phone="+79990000001",
            first_name="Супер",
            last_name="Админ",
            is_staff=True,
            is_superuser=True,
            status_value=UserStatus.ACTIVE,
        )
        cls.regular_user = cls.create_user(
            email="regular@example.com",
            phone="+79990000002",
            first_name="Обычный",
            last_name="Пользователь",
            status_value=UserStatus.ACTIVE,
        )
        cls.student = cls.create_user(
            email="student@example.com",
            phone="+79990000003",
            first_name="Иван",
            last_name="Студентов",
            status_value=UserStatus.ACTIVE,
        )
        cls.teacher = cls.create_user(
            email="teacher@example.com",
            phone="+79990000004",
            first_name="Пётр",
            last_name="Преподавателей",
            status_value=UserStatus.ACTIVE,
        )
        cls.parent = cls.create_user(
            email="parent@example.com",
            phone="+79990000005",
            first_name="Мария",
            last_name="Родителева",
            status_value=UserStatus.ACTIVE,
        )

        UserRole.objects.get_or_create(
            user=cls.superadmin,
            role=cls.superadmin_role,
            defaults={
                "status": UserRoleStatus.ACTIVE,
                "assigned_by": cls.superadmin,
            },
        )
        UserRole.objects.get_or_create(
            user=cls.student,
            role=cls.learner_role,
            defaults={
                "status": UserRoleStatus.ACTIVE,
                "assigned_by": cls.superadmin,
            },
        )
        UserRole.objects.get_or_create(
            user=cls.teacher,
            role=cls.teacher_role,
            defaults={
                "status": UserRoleStatus.ACTIVE,
                "assigned_by": cls.superadmin,
            },
        )
        UserRole.objects.get_or_create(
            user=cls.parent,
            role=cls.guardian_role,
            defaults={
                "status": UserRoleStatus.ACTIVE,
                "assigned_by": cls.superadmin,
            },
        )

    @staticmethod
    def get_or_create_role(
        *,
        code: str,
        label: str,
        description: str = "",
        is_system: bool = True,
        is_active: bool = True,
        sort_order: int = 100,
    ) -> Role:
        """
        Возвращает существующую роль или создаёт её для тестов.

        Системные роли в проекте могут создаваться заранее,
        поэтому нельзя использовать Role.objects.create()
        для фиксированных RoleCode.
        """

        role, _ = Role.objects.update_or_create(
            code=code,
            defaults={
                "label": label,
                "description": description,
                "is_system": is_system,
                "is_active": is_active,
                "sort_order": sort_order,
            },
        )

        return role

    @staticmethod
    def create_user(
        *,
        email: str,
        phone: str,
        first_name: str = "",
        last_name: str = "",
        status_value: str = UserStatus.ACTIVE,
        is_staff: bool = False,
        is_superuser: bool = False,
    ) -> User:
        """
        Создаёт пользователя для тестов.

        В проекте ЦОС «Пифагор» телефон обязателен,
        поэтому helper всегда принимает уникальный phone.
        """

        return User.objects.create_user(
            email=email,
            phone=phone,
            password="TestPassword123!",
            first_name=first_name,
            last_name=last_name,
            status=status_value,
            is_active=status_value == UserStatus.ACTIVE,
            is_staff=is_staff,
            is_superuser=is_superuser,
            is_email_verified=True,
            email_verified_at=timezone.now(),
            is_phone_verified=True,
            phone_verified_at=timezone.now(),
        )

    def get_response_items(self, response) -> list:
        """
        Возвращает список объектов из обычного, пагинированного
        или обёрнутого ответа API.
        """

        data = response.data

        if isinstance(data, list):
            return data

        if not isinstance(data, dict):
            return []

        if "results" in data and isinstance(data["results"], list):
            return data["results"]

        if "items" in data and isinstance(data["items"], list):
            return data["items"]

        nested_data = data.get("data")

        if isinstance(nested_data, list):
            return nested_data

        if isinstance(nested_data, dict):
            if "results" in nested_data and isinstance(nested_data["results"], list):
                return nested_data["results"]

            if "items" in nested_data and isinstance(nested_data["items"], list):
                return nested_data["items"]

        return []

    def get_response_total_count(self, response) -> int:
        """
        Возвращает общее количество объектов из обычного,
        пагинированного или обёрнутого ответа API.
        """

        data = response.data

        if isinstance(data, list):
            return len(data)

        if not isinstance(data, dict):
            return 0

        if "count" in data:
            return int(data["count"])

        if "total_count" in data:
            return int(data["total_count"])

        nested_data = data.get("data")

        if isinstance(nested_data, dict):
            if "count" in nested_data:
                return int(nested_data["count"])

            if "total_count" in nested_data:
                return int(nested_data["total_count"])

        return len(self.get_response_items(response))

    def get_error_message(self, response) -> str:
        """
        Возвращает текст ошибки из стандартного или обёрнутого error-response.
        """

        data = response.data

        if isinstance(data, dict):
            if "error" in data and isinstance(data["error"], dict):
                return str(data["error"].get("message", ""))

            if "detail" in data:
                return str(data["detail"])

            return str(data)

        return str(data)

    def authenticate_as_superadmin(self) -> None:
        """
        Авторизует клиента как суперадминистратора.
        """

        self.client.force_authenticate(user=self.superadmin)

    def authenticate_as_regular_user(self) -> None:
        """
        Авторизует клиента как обычного пользователя.
        """

        self.client.force_authenticate(user=self.regular_user)

    def test_superadmin_can_get_admin_users_list(self):
        """
        Суперадминистратор может получить список пользователей.
        """

        self.authenticate_as_superadmin()

        url = reverse("users:admin-users-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        items = self.get_response_items(response)
        total_count = self.get_response_total_count(response)

        self.assertGreaterEqual(total_count, 4)
        self.assertGreaterEqual(len(items), 1)

    def test_regular_user_cannot_get_admin_users_list(self):
        """
        Обычный пользователь не может открыть административный список.
        """

        self.authenticate_as_regular_user()

        url = reverse("users:admin-users-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_superadmin_can_get_admin_user_detail(self):
        """
        Суперадминистратор может открыть детальную карточку пользователя.
        """

        self.authenticate_as_superadmin()

        url = reverse(
            "users:admin-users-detail",
            kwargs={"pk": self.student.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["id"], self.student.id)
        self.assertEqual(response.data["email"], self.student.email)
        self.assertIn("user_roles", response.data)

    @patch(
        "apps.users.services.admin_users.update_services."
        "send_email_verification_task.delay"
    )
    def test_superadmin_can_update_user_base_fields(self, mocked_email_task):
        """
        Суперадминистратор может изменить базовые данные пользователя.
        """

        self.authenticate_as_superadmin()

        url = reverse(
            "users:admin-users-detail",
            kwargs={"pk": self.student.id},
        )
        payload = {
            "first_name": "Алексей",
            "last_name": "Обновлённый",
            "reason": "Исправление данных пользователя.",
        }

        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.student.refresh_from_db()

        self.assertEqual(self.student.first_name, "Алексей")
        self.assertEqual(self.student.last_name, "Обновлённый")
        mocked_email_task.assert_not_called()

        self.assertTrue(
            UserAuditLog.objects.filter(
                target_user=self.student,
                actor=self.superadmin,
                action=UserAuditAction.PROFILE_UPDATED,
            ).exists()
        )

    def test_superadmin_can_update_backup_email_with_timezone_expected_updated_at(self):
        """
        PATCH сохраняет резервный email, если expected_updated_at передан в другом timezone.
        """

        self.authenticate_as_superadmin()

        expected_updated_at = self.student.updated_at.astimezone(
            ZoneInfo("Europe/Moscow")
        ).isoformat()

        url = reverse(
            "users:admin-users-detail",
            kwargs={"pk": self.student.id},
        )
        payload = {
            "backup_email": "student.backup@example.com",
            "expected_updated_at": expected_updated_at,
            "reason": "Добавление резервной почты.",
        }

        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.student.refresh_from_db()

        self.assertEqual(self.student.backup_email, "student.backup@example.com")

    @patch(
        "apps.users.services.admin_users.update_services."
        "send_email_verification_task.delay"
    )
    def test_superadmin_email_change_requires_new_verification(
        self,
        mocked_email_task,
    ):
        """
        При смене email администратором email снова требует подтверждения.
        """

        self.authenticate_as_superadmin()

        old_email = self.student.email

        url = reverse(
            "users:admin-users-detail",
            kwargs={"pk": self.student.id},
        )
        payload = {
            "email": "new-student@example.com",
            "reason": "Замена email по заявке.",
        }

        with self.captureOnCommitCallbacks(execute=True):
            response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.student.refresh_from_db()

        self.assertEqual(self.student.email, "new-student@example.com")
        self.assertFalse(self.student.is_email_verified)
        self.assertIsNone(self.student.email_verified_at)
        self.assertEqual(self.student.status, UserStatus.PENDING_EMAIL)

        mocked_email_task.assert_called_once_with(user_id=self.student.id)

        self.assertTrue(
            UserAuditLog.objects.filter(
                target_user=self.student,
                actor=self.superadmin,
                action=UserAuditAction.PROFILE_UPDATED,
                metadata__old_email=old_email,
                metadata__new_email="new-student@example.com",
            ).exists()
        )

    def test_update_user_returns_error_when_expected_updated_at_is_stale(self):
        """
        PATCH возвращает ошибку, если пользователь уже был изменён другим админом.
        """

        self.authenticate_as_superadmin()

        stale_updated_at = (self.student.updated_at - timedelta(minutes=5)).isoformat()

        url = reverse(
            "users:admin-users-detail",
            kwargs={"pk": self.student.id},
        )
        payload = {
            "first_name": "Конфликт",
            "expected_updated_at": stale_updated_at,
        }

        response = self.client.patch(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        error_message = self.get_error_message(response)

        self.assertIn(
            "Пользователь уже был изменён другим администратором",
            error_message,
        )

    def test_superadmin_can_block_user(self):
        """
        Суперадминистратор может заблокировать пользователя.
        """

        self.authenticate_as_superadmin()

        url = reverse(
            "users:admin-users-block",
            kwargs={"pk": self.student.id},
        )
        payload = {
            "reason": "Нарушение правил платформы.",
            "expected_updated_at": self.student.updated_at.isoformat(),
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.student.refresh_from_db()

        self.assertEqual(self.student.status, UserStatus.BLOCKED)
        self.assertFalse(self.student.is_active)

        self.assertTrue(
            UserAuditLog.objects.filter(
                target_user=self.student,
                actor=self.superadmin,
                action=UserAuditAction.USER_BLOCKED,
            ).exists()
        )

    def test_superadmin_can_unblock_user(self):
        """
        Суперадминистратор может разблокировать пользователя.
        """

        self.student.status = UserStatus.BLOCKED
        self.student.is_active = False
        self.student.save(update_fields=["status", "is_active", "updated_at"])

        self.authenticate_as_superadmin()

        url = reverse(
            "users:admin-users-unblock",
            kwargs={"pk": self.student.id},
        )
        payload = {
            "reason": "Проверка завершена.",
            "expected_updated_at": self.student.updated_at.isoformat(),
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.student.refresh_from_db()

        self.assertEqual(self.student.status, UserStatus.ACTIVE)
        self.assertTrue(self.student.is_active)

        self.assertTrue(
            UserAuditLog.objects.filter(
                target_user=self.student,
                actor=self.superadmin,
                action=UserAuditAction.USER_UNBLOCKED,
            ).exists()
        )

    def test_superadmin_can_archive_user(self):
        """
        Суперадминистратор может архивировать пользователя.
        """

        self.authenticate_as_superadmin()

        url = reverse(
            "users:admin-users-archive",
            kwargs={"pk": self.teacher.id},
        )
        payload = {
            "reason": "Пользователь больше не работает в организации.",
            "expected_updated_at": self.teacher.updated_at.isoformat(),
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.teacher.refresh_from_db()

        self.assertEqual(self.teacher.status, UserStatus.ARCHIVED)
        self.assertFalse(self.teacher.is_active)

        self.assertTrue(
            UserAuditLog.objects.filter(
                target_user=self.teacher,
                actor=self.superadmin,
                action=UserAuditAction.USER_ARCHIVED,
            ).exists()
        )

    def test_superadmin_can_restore_archived_user(self):
        """
        Суперадминистратор может восстановить архивного пользователя.
        """

        self.teacher.status = UserStatus.ARCHIVED
        self.teacher.is_active = False
        self.teacher.save(update_fields=["status", "is_active", "updated_at"])

        self.authenticate_as_superadmin()

        url = reverse(
            "users:admin-users-restore",
            kwargs={"pk": self.teacher.id},
        )
        payload = {
            "reason": "Пользователь вернулся в организацию.",
            "expected_updated_at": self.teacher.updated_at.isoformat(),
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.teacher.refresh_from_db()

        self.assertEqual(self.teacher.status, UserStatus.ACTIVE)
        self.assertTrue(self.teacher.is_active)

        self.assertTrue(
            UserAuditLog.objects.filter(
                target_user=self.teacher,
                actor=self.superadmin,
                action=UserAuditAction.USER_RESTORED,
            ).exists()
        )

    def test_superadmin_can_schedule_user_deletion(self):
        """
        DELETE не удаляет пользователя физически, а планирует удаление.
        """

        self.authenticate_as_superadmin()

        url = reverse(
            "users:admin-users-detail",
            kwargs={"pk": self.parent.id},
        )
        payload = {
            "reason": "Удаление по заявке.",
            "expected_updated_at": self.parent.updated_at.isoformat(),
        }

        response = self.client.delete(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_202_ACCEPTED)

        self.parent.refresh_from_db()

        self.assertEqual(self.parent.status, UserStatus.SCHEDULED_FOR_DELETION)
        self.assertFalse(self.parent.is_active)
        self.assertIsNotNone(self.parent.scheduled_for_deletion_at)

        self.assertTrue(
            UserAuditLog.objects.filter(
                target_user=self.parent,
                actor=self.superadmin,
                action=UserAuditAction.USER_SCHEDULED_FOR_DELETION,
            ).exists()
        )

        self.assertTrue(User.objects.filter(id=self.parent.id).exists())

    def test_superadmin_cannot_delete_self(self):
        """
        Суперадминистратор не может запланировать удаление собственного аккаунта.
        """

        self.authenticate_as_superadmin()

        url = reverse(
            "users:admin-users-detail",
            kwargs={"pk": self.superadmin.id},
        )
        payload = {
            "reason": "Попытка удалить себя.",
            "expected_updated_at": self.superadmin.updated_at.isoformat(),
        }

        response = self.client.delete(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        self.superadmin.refresh_from_db()

        self.assertNotEqual(
            self.superadmin.status,
            UserStatus.SCHEDULED_FOR_DELETION,
        )

    def test_superadmin_can_change_user_roles(self):
        """
        Суперадминистратор может назначить пользователю новую роль.
        """

        self.authenticate_as_superadmin()

        url = reverse(
            "users:admin-users-change-roles",
            kwargs={"pk": self.student.id},
        )
        payload = {
            "assigned_roles": [
                {
                    "role_id": self.teacher_role.id,
                    "organization_id": None,
                    "department_id": None,
                    "group_id": None,
                }
            ],
            "reason": "Пользователь совмещает роли.",
            "expected_updated_at": self.student.updated_at.isoformat(),
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.assertTrue(
            UserRole.objects.filter(
                user=self.student,
                role=self.teacher_role,
                status=UserRoleStatus.ACTIVE,
            ).exists()
        )

        self.assertTrue(
            UserAuditLog.objects.filter(
                target_user=self.student,
                actor=self.superadmin,
                action=UserAuditAction.ROLE_ASSIGNED,
            ).exists()
        )

    def test_superadmin_can_revoke_user_role(self):
        """
        Суперадминистратор может отозвать роль пользователя.
        """

        user_role = UserRole.objects.get(
            user=self.student,
            role=self.learner_role,
        )

        self.authenticate_as_superadmin()

        url = reverse(
            "users:admin-users-change-roles",
            kwargs={"pk": self.student.id},
        )
        payload = {
            "revoked_user_role_ids": [user_role.id],
            "reason": "Роль больше не актуальна.",
            "expected_updated_at": self.student.updated_at.isoformat(),
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        user_role.refresh_from_db()

        self.assertEqual(user_role.status, UserRoleStatus.REVOKED)
        self.assertEqual(user_role.revoked_by, self.superadmin)
        self.assertIsNotNone(user_role.revoked_at)

        self.assertTrue(
            UserAuditLog.objects.filter(
                target_user=self.student,
                actor=self.superadmin,
                action=UserAuditAction.ROLE_REVOKED,
            ).exists()
        )

    def test_superadmin_can_run_bulk_block(self):
        """
        Суперадминистратор может массово заблокировать пользователей.
        """

        self.authenticate_as_superadmin()

        url = reverse("users:admin-users-bulk")
        payload = {
            "action": "block",
            "user_ids": [
                self.student.id,
                self.teacher.id,
            ],
            "reason": "Массовая блокировка тестовых пользователей.",
            "expected_updated_at_by_user_id": {
                str(self.student.id): self.student.updated_at.isoformat(),
                str(self.teacher.id): self.teacher.updated_at.isoformat(),
            },
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_count"], 2)
        self.assertEqual(response.data["success_count"], 2)
        self.assertEqual(response.data["failed_count"], 0)

        self.student.refresh_from_db()
        self.teacher.refresh_from_db()

        self.assertEqual(self.student.status, UserStatus.BLOCKED)
        self.assertEqual(self.teacher.status, UserStatus.BLOCKED)

    def test_bulk_action_returns_partial_failures(self):
        """
        Bulk-действие возвращает частичные ошибки, если часть пользователей недоступна.
        """

        self.authenticate_as_superadmin()

        unknown_user_id = 999999

        url = reverse("users:admin-users-bulk")
        payload = {
            "action": "archive",
            "user_ids": [
                self.student.id,
                unknown_user_id,
            ],
            "reason": "Проверка частичного выполнения.",
            "expected_updated_at_by_user_id": {
                str(self.student.id): self.student.updated_at.isoformat(),
            },
        }

        response = self.client.post(url, payload, format="json")

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["total_count"], 2)
        self.assertEqual(response.data["success_count"], 1)
        self.assertEqual(response.data["failed_count"], 1)

        failed_items = [item for item in response.data["items"] if not item["success"]]

        self.assertEqual(len(failed_items), 1)
        self.assertEqual(failed_items[0]["user_id"], unknown_user_id)

    def test_available_roles_returns_active_roles(self):
        """
        Endpoint available-roles возвращает активные роли.
        """

        self.authenticate_as_superadmin()

        url = reverse("users:admin-users-available-roles")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        items = self.get_response_items(response)

        if not items and isinstance(response.data, list):
            items = response.data

        role_codes = {item["code"] for item in items}

        self.assertIn(RoleCode.LEARNER, role_codes)
        self.assertIn(RoleCode.TEACHER, role_codes)
        self.assertIn(RoleCode.GUARDIAN, role_codes)

    def test_audit_logs_endpoint_returns_user_history(self):
        """
        Endpoint audit-logs возвращает историю действий по пользователю.
        """

        UserAuditLog.objects.create(
            actor=self.superadmin,
            target_user=self.student,
            action=UserAuditAction.PROFILE_UPDATED,
            actor_type="admin",
            message="Тестовая запись аудита.",
            metadata={"source": "test"},
        )

        self.authenticate_as_superadmin()

        url = reverse(
            "users:admin-users-audit-logs",
            kwargs={"pk": self.student.id},
        )
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        items = self.get_response_items(response)

        self.assertGreaterEqual(len(items), 1)

    def test_students_filter_returns_only_students(self):
        """
        Фильтр role_group=students возвращает пользователей с ролью студента.
        """

        self.authenticate_as_superadmin()

        url = reverse("users:admin-users-list")
        response = self.client.get(
            url,
            {
                "role_group": "students",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        items = self.get_response_items(response)

        emails = {item["email"] for item in items}

        self.assertIn(self.student.email, emails)
        self.assertNotIn(self.teacher.email, emails)
        self.assertNotIn(self.parent.email, emails)

    def test_teachers_filter_returns_only_teachers(self):
        """
        Фильтр role_group=teachers возвращает пользователей с преподавательскими ролями.
        """

        self.authenticate_as_superadmin()

        url = reverse("users:admin-users-list")
        response = self.client.get(
            url,
            {
                "role_group": "teachers",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        items = self.get_response_items(response)

        emails = {item["email"] for item in items}

        self.assertIn(self.teacher.email, emails)
        self.assertNotIn(self.student.email, emails)
        self.assertNotIn(self.parent.email, emails)

    def test_parents_filter_returns_only_parents(self):
        """
        Фильтр role_group=parents возвращает пользователей с ролью родителя.
        """

        self.authenticate_as_superadmin()

        url = reverse("users:admin-users-list")
        response = self.client.get(
            url,
            {
                "role_group": "parents",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        items = self.get_response_items(response)

        emails = {item["email"] for item in items}

        self.assertIn(self.parent.email, emails)
        self.assertNotIn(self.student.email, emails)
        self.assertNotIn(self.teacher.email, emails)
