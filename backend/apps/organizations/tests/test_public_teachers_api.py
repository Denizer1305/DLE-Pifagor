from __future__ import annotations

from apps.organizations.models import Organization, Subject, TeacherSubject
from apps.organizations.tests.factories import create_test_user
from apps.users.constants.lifecycle import ProfileStatus
from apps.users.models import TeacherProfile
from django.test import TestCase
from rest_framework.test import APIClient


class PublicTeachersApiTestCase(TestCase):
    def setUp(self) -> None:
        self.client = APIClient()

        self.default_organization = Organization.objects.create(
            name="ГАПОУ ВО «ВлГК им. Д.К. Советкина»",
            short_name="ВлГК им. Советкина",
            code="vlgk_sovetkina",
            slug="vlgk-sovetkina",
            city="Владимир",
            is_active=True,
            is_public=True,
            is_default_public=True,
        )

        self.other_organization = Organization.objects.create(
            name="Другая образовательная организация",
            short_name="Другая организация",
            code="other_org",
            slug="other-org",
            is_active=True,
            is_public=True,
            is_default_public=False,
        )

        self.math = Subject.objects.create(
            name="Математика",
            short_name="Математика",
            code="math",
            is_active=True,
        )

        self.physics = Subject.objects.create(
            name="Физика",
            short_name="Физика",
            code="physics",
            is_active=True,
        )

        self.teacher = create_test_user(
            email="teacher@example.com",
            phone="+79990000003",
            first_name="Иван",
            last_name="Иванов",
            middle_name="Иванович",
        )

        self.teacher_profile = TeacherProfile.objects.create(
            user=self.teacher,
            organization=self.default_organization,
            status=ProfileStatus.VERIFIED,
            position="Преподаватель математики",
            public_title="Преподаватель точных наук",
            short_bio="Помогает студентам спокойно разобраться в математике.",
            achievements=(
                "Победитель профессионального конкурса\n"
                "Автор методических материалов"
            ),
            experience_years=7,
            is_public=True,
            show_on_teachers_page=True,
        )

        TeacherSubject.objects.create(
            teacher=self.teacher,
            subject=self.math,
            is_primary=True,
            is_active=True,
        )

        TeacherSubject.objects.create(
            teacher=self.teacher,
            subject=self.physics,
            is_primary=False,
            is_active=True,
        )

        self.hidden_teacher = create_test_user(
            email="hidden@example.com",
            phone="+79990000004",
            first_name="Пётр",
            last_name="Петров",
            middle_name="Петрович",
        )

        TeacherProfile.objects.create(
            user=self.hidden_teacher,
            organization=self.default_organization,
            status=ProfileStatus.VERIFIED,
            position="Скрытый преподаватель",
            is_public=False,
            show_on_teachers_page=True,
        )

        self.other_teacher = create_test_user(
            email="other@example.com",
            phone="+79990000005",
            first_name="Анна",
            last_name="Сидорова",
            middle_name="Андреевна",
        )

        TeacherProfile.objects.create(
            user=self.other_teacher,
            organization=self.other_organization,
            status=ProfileStatus.VERIFIED,
            position="Преподаватель другой организации",
            is_public=True,
            show_on_teachers_page=True,
        )

    def test_public_teachers_page_for_anonymous_user_uses_default_organization(
        self,
    ) -> None:
        response = self.client.get("/api/v1/organizations/public/teachers/")

        self.assertEqual(response.status_code, 200)

        payload = response.json()

        self.assertEqual(payload["organization"]["id"], self.default_organization.id)
        self.assertTrue(payload["meta"]["is_fallback"])
        self.assertEqual(payload["meta"]["teachers_count"], 1)
        self.assertEqual(len(payload["teachers"]), 1)

        teacher = payload["teachers"][0]

        self.assertEqual(teacher["full_name"], "Иванов Иван Иванович")
        self.assertEqual(teacher["position"], "Преподаватель точных наук")
        self.assertEqual(
            teacher["description"],
            "Помогает студентам спокойно разобраться в математике.",
        )
        self.assertEqual(teacher["experience_years"], 7)
        self.assertEqual(len(teacher["subjects"]), 2)
        self.assertEqual(len(teacher["achievements"]), 2)

    def test_public_teachers_page_does_not_return_hidden_teachers(self) -> None:
        response = self.client.get("/api/v1/organizations/public/teachers/")

        self.assertEqual(response.status_code, 200)

        payload = response.json()

        teacher_ids = [teacher["id"] for teacher in payload["teachers"]]

        self.assertIn(self.teacher.id, teacher_ids)
        self.assertNotIn(self.hidden_teacher.id, teacher_ids)

    def test_public_teachers_page_filters_by_search(self) -> None:
        response = self.client.get(
            "/api/v1/organizations/public/teachers/",
            {
                "search": "математике",
            },
        )

        self.assertEqual(response.status_code, 200)

        payload = response.json()

        self.assertEqual(payload["meta"]["teachers_count"], 1)
        self.assertEqual(payload["teachers"][0]["id"], self.teacher.id)

    def test_public_teachers_page_filters_by_subject_code(self) -> None:
        response = self.client.get(
            "/api/v1/organizations/public/teachers/",
            {
                "subject": "math",
            },
        )

        self.assertEqual(response.status_code, 200)

        payload = response.json()

        self.assertEqual(payload["meta"]["teachers_count"], 1)
        self.assertEqual(payload["teachers"][0]["id"], self.teacher.id)

    def test_public_teachers_page_returns_empty_list_for_unknown_subject(self) -> None:
        response = self.client.get(
            "/api/v1/organizations/public/teachers/",
            {
                "subject": "unknown_subject",
            },
        )

        self.assertEqual(response.status_code, 200)

        payload = response.json()

        self.assertEqual(payload["meta"]["teachers_count"], 0)
        self.assertEqual(payload["teachers"], [])

    def test_public_teachers_page_filters_by_position(self) -> None:
        response = self.client.get(
            "/api/v1/organizations/public/teachers/",
            {
                "position": "математики",
            },
        )

        self.assertEqual(response.status_code, 200)

        payload = response.json()

        self.assertEqual(payload["meta"]["teachers_count"], 1)
        self.assertEqual(payload["teachers"][0]["id"], self.teacher.id)

    def test_public_teachers_page_for_authorized_user_uses_user_organization(
        self,
    ) -> None:
        self.client.force_authenticate(user=self.other_teacher)

        response = self.client.get("/api/v1/organizations/public/teachers/")

        self.assertEqual(response.status_code, 200)

        payload = response.json()

        self.assertEqual(payload["organization"]["id"], self.other_organization.id)
        self.assertFalse(payload["meta"]["is_fallback"])
        self.assertEqual(payload["meta"]["teachers_count"], 1)
        self.assertEqual(payload["teachers"][0]["id"], self.other_teacher.id)

    def test_public_teacher_subjects_are_returned_for_filters(self) -> None:
        response = self.client.get("/api/v1/organizations/public/teachers/")

        self.assertEqual(response.status_code, 200)

        payload = response.json()

        subject_codes = {subject["code"] for subject in payload["subjects"]}

        self.assertEqual(subject_codes, {"math", "physics"})
        self.assertEqual(payload["meta"]["subjects_count"], 2)

    def test_public_teachers_page_does_not_return_unverified_teachers(self) -> None:
        unverified_teacher = create_test_user(
            email="unverified@example.com",
            phone="+79990000006",
            first_name="Сергей",
            last_name="Сергеев",
            middle_name="Сергеевич",
        )

        TeacherProfile.objects.create(
            user=unverified_teacher,
            organization=self.default_organization,
            status=ProfileStatus.PENDING_REVIEW,
            position="Преподаватель на проверке",
            is_public=True,
            show_on_teachers_page=True,
        )

        response = self.client.get("/api/v1/organizations/public/teachers/")

        self.assertEqual(response.status_code, 200)

        payload = response.json()

        teacher_ids = [teacher["id"] for teacher in payload["teachers"]]

        self.assertIn(self.teacher.id, teacher_ids)
        self.assertNotIn(unverified_teacher.id, teacher_ids)
