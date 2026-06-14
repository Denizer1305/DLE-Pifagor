from __future__ import annotations

from apps.users.constants.lifecycle import UserRoleStatus, UserStatus
from apps.users.constants.roles import RoleCode
from apps.users.models import UserRole
from apps.users.tests.factories import make_role, make_user
from rest_framework.test import APITestCase


class BackofficeUsersApiTestCase(APITestCase):
    """
    Базовый test case для API backoffice/users.
    """

    @classmethod
    def setUpTestData(cls):
        """
        Подготавливает пользователей и роли.
        """

        cls.superadmin_role = make_role(code=RoleCode.SUPERADMIN)
        cls.learner_role = make_role(code=RoleCode.LEARNER)
        cls.teacher_role = make_role(code=RoleCode.TEACHER)
        cls.guardian_role = make_role(code=RoleCode.GUARDIAN)

        cls.superadmin = make_user(
            email="backoffice.superadmin@example.com",
            phone="+79991000001",
            first_name="Супер",
            last_name="Админ",
            status=UserStatus.ACTIVE,
            is_active=True,
            is_staff=True,
            is_superuser=True,
        )
        cls.regular_user = make_user(
            email="backoffice.regular@example.com",
            phone="+79991000002",
            first_name="Обычный",
            last_name="Пользователь",
            status=UserStatus.ACTIVE,
            is_active=True,
        )
        cls.student = make_user(
            email="backoffice.student@example.com",
            phone="+79991000003",
            first_name="Иван",
            last_name="Студентов",
            status=UserStatus.ACTIVE,
            is_active=True,
        )
        cls.teacher = make_user(
            email="backoffice.teacher@example.com",
            phone="+79991000004",
            first_name="Пётр",
            last_name="Преподавателей",
            status=UserStatus.ACTIVE,
            is_active=True,
        )
        cls.parent = make_user(
            email="backoffice.parent@example.com",
            phone="+79991000005",
            first_name="Мария",
            last_name="Родителева",
            status=UserStatus.ACTIVE,
            is_active=True,
        )

        cls.assign_role(cls.superadmin, cls.superadmin_role)
        cls.assign_role(cls.student, cls.learner_role)
        cls.assign_role(cls.teacher, cls.teacher_role)
        cls.assign_role(cls.parent, cls.guardian_role)

    @classmethod
    def assign_role(cls, user, role) -> UserRole:
        """
        Назначает пользователю активную роль.
        """

        user_role, _created = UserRole.objects.get_or_create(
            user=user,
            role=role,
            defaults={
                "status": UserRoleStatus.ACTIVE,
                "assigned_by": cls.superadmin,
            },
        )

        return user_role

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

    def get_response_items(self, response) -> list:
        """
        Возвращает список объектов из обычного или пагинированного ответа.
        """

        data = response.data

        if isinstance(data, list):
            return data

        if not isinstance(data, dict):
            return []

        if isinstance(data.get("results"), list):
            return data["results"]

        if isinstance(data.get("items"), list):
            return data["items"]

        nested_data = data.get("data")

        if isinstance(nested_data, list):
            return nested_data

        if isinstance(nested_data, dict):
            if isinstance(nested_data.get("results"), list):
                return nested_data["results"]

            if isinstance(nested_data.get("items"), list):
                return nested_data["items"]

        return []

    def get_response_total_count(self, response) -> int:
        """
        Возвращает total count из ответа API.
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
