from __future__ import annotations

from apps.education.permissions.shared import (
    user_can_access_learner_enrollment,
    user_can_access_object_by_group,
    user_can_access_object_by_organization,
    user_can_access_teacher_assignment,
    user_can_manage_global_education,
    user_can_manage_scoped_education,
    user_has_education_access,
)
from apps.education.tests.factories import (
    create_curriculum,
    create_learner_group_enrollment,
    create_teacher_group_subject,
    create_user,
)
from django.test import TestCase


class EducationPermissionsTestCase(TestCase):
    """
    Тесты permission helpers академического модуля.
    """

    def test_superadmin_can_manage_global_education(self) -> None:
        """
        Суперадмин может управлять глобальными академическими сущностями.
        """

        user = create_user(role_code="superadmin")

        self.assertTrue(user_has_education_access(user))
        self.assertTrue(user_can_manage_global_education(user))
        self.assertTrue(user_can_manage_scoped_education(user))

    def test_learner_has_read_access_but_not_manage_access(self) -> None:
        """
        Обучающийся имеет академический доступ, но не управляет данными.
        """

        user = create_user(role_code="learner")

        self.assertTrue(user_has_education_access(user))
        self.assertFalse(user_can_manage_global_education(user))
        self.assertFalse(user_can_manage_scoped_education(user))

    def test_user_can_access_object_by_organization(self) -> None:
        """
        Пользователь с доступом к организации видит объект организации.
        """

        user = create_user(role_code="superadmin")
        curriculum = create_curriculum()

        self.assertTrue(
            user_can_access_object_by_organization(
                user=user,
                obj=curriculum,
            )
        )

    def test_user_can_access_object_by_group(self) -> None:
        """
        Пользователь с доступом к группе видит объект группы.
        """

        user = create_user(role_code="superadmin")
        enrollment = create_learner_group_enrollment()

        self.assertTrue(
            user_can_access_object_by_group(
                user=user,
                obj=enrollment,
            )
        )

    def test_teacher_can_access_own_assignment(self) -> None:
        """
        Преподаватель имеет доступ к своему назначению.
        """

        teacher = create_user(role_code="teacher")
        assignment = create_teacher_group_subject(teacher=teacher)

        self.assertTrue(
            user_can_access_teacher_assignment(
                user=teacher,
                obj=assignment,
            )
        )

    def test_learner_can_access_own_enrollment(self) -> None:
        """
        Обучающийся имеет доступ к своему зачислению.
        """

        learner = create_user(role_code="learner")
        enrollment = create_learner_group_enrollment(learner=learner)

        self.assertTrue(
            user_can_access_learner_enrollment(
                user=learner,
                obj=enrollment,
            )
        )
