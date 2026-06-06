from __future__ import annotations

from apps.organizations.tests.factories import (
    create_organization,
    create_subject,
    create_teacher,
    create_teacher_subject,
)
from apps.users.constants.lifecycle import ProfileStatus
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient


class PublicTeachersApiTestCase(TestCase):
    """
    Тесты публичной страницы преподавателей.
    """

    def setUp(self) -> None:
        self.client = APIClient()

        self.default_organization = create_organization(
            name="ГАПОУ ВО «ВлГК им. Д.К. Советкина»",
            short_name="ВлГК им. Советкина",
            code="vlgk_sovetkina",
            slug="vlgk-sovetkina",
            city="Владимир",
            is_active=True,
            is_public=True,
            is_default_public=True,
        )

        self.other_organization = create_organization(
            name="Другая образовательная организация",
            short_name="Другая организация",
            code="other_org",
            slug="other-org",
            is_active=True,
            is_public=True,
            is_default_public=False,
        )

        self.math = create_subject(
            name="Математика",
            short_name="Математика",
            code="math",
        )
        self.physics = create_subject(
            name="Физика",
            short_name="Физика",
            code="physics",
        )

        self.teacher = create_teacher(
            organization=self.default_organization,
            email="teacher@example.com",
            phone="+79990000020",
            first_name="Иван",
            last_name="Иванов",
            middle_name="Иванович",
            position="Преподаватель точных наук",
        )
        create_teacher_subject(
            teacher=self.teacher,
            subject=self.math,
            is_primary=True,
        )
        create_teacher_subject(
            teacher=self.teacher,
            subject=self.physics,
            is_primary=False,
        )

        self.hidden_teacher = create_teacher(
            organization=self.default_organization,
            email="hidden@example.com",
            phone="+79990000021",
            first_name="Пётр",
            last_name="Петров",
            middle_name="Петрович",
            position="Скрытый преподаватель",
            is_public=False,
            show_on_teachers_page=True,
        )

        self.unverified_teacher = create_teacher(
            organization=self.default_organization,
            email="unverified@example.com",
            phone="+79990000022",
            first_name="Сергей",
            last_name="Сергеев",
            middle_name="Сергеевич",
            position="Преподаватель на проверке",
            status=ProfileStatus.PENDING_REVIEW,
        )

        self.other_teacher = create_teacher(
            organization=self.other_organization,
            email="other@example.com",
            phone="+79990000023",
            first_name="Анна",
            last_name="Сидорова",
            middle_name="Андреевна",
            position="Преподаватель другой организации",
        )

    def test_anonymous_user_uses_default_public_organization(self) -> None:
        """
        Анонимный пользователь получает преподавателей default_public организации.
        """

        url = reverse("organizations:public-teachers-page")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["organization"]["id"], self.default_organization.id)
        self.assertTrue(payload["meta"]["is_fallback"])
        self.assertEqual(payload["meta"]["teachers_count"], 1)
        self.assertEqual(len(payload["teachers"]), 1)

        teacher = payload["teachers"][0]

        self.assertEqual(teacher["id"], self.teacher.id)
        self.assertEqual(teacher["full_name"], "Иванов Иван Иванович")
        self.assertEqual(teacher["position"], "Преподаватель точных наук")
        self.assertEqual(len(teacher["subjects"]), 2)

    def test_hidden_teacher_is_not_returned(self) -> None:
        """
        Скрытый преподаватель не попадает на публичную страницу.
        """

        url = reverse("organizations:public-teachers-page")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        teacher_ids = {
            teacher["id"]
            for teacher in response.json()["teachers"]
        }

        self.assertIn(self.teacher.id, teacher_ids)
        self.assertNotIn(self.hidden_teacher.id, teacher_ids)

    def test_unverified_teacher_is_not_returned(self) -> None:
        """
        Неподтверждённый преподаватель не попадает на публичную страницу.
        """

        url = reverse("organizations:public-teachers-page")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        teacher_ids = {
            teacher["id"]
            for teacher in response.json()["teachers"]
        }

        self.assertIn(self.teacher.id, teacher_ids)
        self.assertNotIn(self.unverified_teacher.id, teacher_ids)

    def test_filter_by_search(self) -> None:
        """
        Поиск фильтрует преподавателей по описанию/должности/ФИО.
        """

        url = reverse("organizations:public-teachers-page")

        response = self.client.get(
            url,
            {
                "search": "точных",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["meta"]["teachers_count"], 1)
        self.assertEqual(payload["teachers"][0]["id"], self.teacher.id)

    def test_filter_by_position(self) -> None:
        """
        Фильтр по должности возвращает подходящих преподавателей.
        """

        url = reverse("organizations:public-teachers-page")

        response = self.client.get(
            url,
            {
                "position": "точных",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["meta"]["teachers_count"], 1)
        self.assertEqual(payload["teachers"][0]["id"], self.teacher.id)

    def test_filter_by_subject_code(self) -> None:
        """
        Фильтр по предмету возвращает преподавателя этого предмета.
        """

        url = reverse("organizations:public-teachers-page")

        response = self.client.get(
            url,
            {
                "subject": "math",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["meta"]["teachers_count"], 1)
        self.assertEqual(payload["teachers"][0]["id"], self.teacher.id)

    def test_unknown_subject_returns_empty_teachers_list(self) -> None:
        """
        Неизвестный предмет возвращает пустой список преподавателей.
        """

        url = reverse("organizations:public-teachers-page")

        response = self.client.get(
            url,
            {
                "subject": "unknown_subject",
            },
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["meta"]["teachers_count"], 0)
        self.assertEqual(payload["teachers"], [])

    def test_subjects_are_returned_for_filters(self) -> None:
        """
        Endpoint возвращает предметы для фильтров.
        """

        url = reverse("organizations:public-teachers-page")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()
        subject_codes = {
            subject["code"]
            for subject in payload["subjects"]
        }

        self.assertEqual(subject_codes, {"math", "physics"})
        self.assertEqual(payload["meta"]["subjects_count"], 2)

    def test_authorized_user_uses_own_organization(self) -> None:
        """
        Авторизованный пользователь получает преподавателей своей организации.
        """

        self.client.force_authenticate(user=self.other_teacher)

        url = reverse("organizations:public-teachers-page")

        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = response.json()

        self.assertEqual(payload["organization"]["id"], self.other_organization.id)
        self.assertFalse(payload["meta"]["is_fallback"])
        self.assertEqual(payload["meta"]["teachers_count"], 1)
        self.assertEqual(payload["teachers"][0]["id"], self.other_teacher.id)