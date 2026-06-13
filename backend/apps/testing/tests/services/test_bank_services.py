from __future__ import annotations

from apps.testing.constants import BankItemStatus
from apps.testing.models import TestQuestion as QuestionModel
from apps.testing.services.bank import archive_bank_item, copy_bank_item_to_test
from apps.testing.services.bank import create_bank_item as create_bank_item_service
from apps.testing.services.bank import create_bank_option as create_bank_option_service
from apps.testing.services.bank import (
    duplicate_bank_item,
    publish_bank_item,
    restore_bank_item,
    update_bank_item,
    update_bank_option,
)
from apps.testing.tests.factories import create_bank_item as create_bank_item_factory
from apps.testing.tests.factories import create_bank_item_with_options
from apps.testing.tests.factories import (
    create_bank_option as create_bank_option_factory,
)
from apps.testing.tests.factories import create_published_bank_item, create_test
from django.core.exceptions import ValidationError
from django.test import TestCase


class QuestionBankMutationServicesTestCase(TestCase):
    """
    Тесты сервисов создания и обновления банка заданий.
    """

    def test_create_bank_item_creates_item(self) -> None:
        """
        Сервис создаёт шаблон вопроса.
        """

        exam = create_test()

        bank_item = create_bank_item_service(
            data={
                "title": "Шаблон вопроса",
                "text": "Сколько будет 2 + 2?",
                "organization": exam.organization,
                "subject": exam.subject,
                "owner_teacher": exam.owner_teacher,
            }
        )

        self.assertEqual(bank_item.title, "Шаблон вопроса")
        self.assertEqual(bank_item.organization, exam.organization)
        self.assertEqual(bank_item.subject, exam.subject)

    def test_update_bank_item_updates_title(self) -> None:
        """
        Сервис обновляет шаблон вопроса.
        """

        bank_item = create_bank_item_factory(title="Старое название")

        updated_item = update_bank_item(
            bank_item=bank_item,
            data={
                "title": "Новое название",
            },
        )

        self.assertEqual(updated_item.title, "Новое название")

    def test_create_bank_option_creates_option(self) -> None:
        """
        Сервис создаёт вариант ответа шаблона.
        """

        bank_item = create_bank_item_factory(score=2)

        option = create_bank_option_service(
            data={
                "bank_item": bank_item,
                "text": "4",
                "order": 1,
                "is_correct": True,
                "score": 1,
            }
        )

        self.assertEqual(option.bank_item, bank_item)
        self.assertEqual(option.text, "4")
        self.assertTrue(option.is_correct)

    def test_update_bank_option_updates_text(self) -> None:
        """
        Сервис обновляет вариант ответа шаблона.
        """

        option = create_bank_option_factory(text="Старый ответ")

        updated_option = update_bank_option(
            option=option,
            data={
                "text": "Новый ответ",
            },
        )

        self.assertEqual(updated_option.text, "Новый ответ")


class QuestionBankStatusServicesTestCase(TestCase):
    """
    Тесты сервисов статусов банка заданий.
    """

    def test_publish_bank_item_sets_published_status(self) -> None:
        """
        Сервис публикует шаблон вопроса.
        """

        bank_item = create_bank_item_with_options()

        published_item = publish_bank_item(bank_item=bank_item)

        self.assertEqual(published_item.status, BankItemStatus.PUBLISHED)
        self.assertTrue(published_item.is_active)
        self.assertIsNotNone(published_item.published_at)
        self.assertIsNone(published_item.archived_at)

    def test_archive_bank_item_sets_archived_status(self) -> None:
        """
        Сервис архивирует шаблон вопроса.
        """

        bank_item = create_published_bank_item()

        archived_item = archive_bank_item(bank_item=bank_item)

        self.assertEqual(archived_item.status, BankItemStatus.ARCHIVED)
        self.assertFalse(archived_item.is_active)
        self.assertIsNotNone(archived_item.archived_at)

    def test_restore_bank_item_returns_item_to_draft(self) -> None:
        """
        Сервис восстанавливает шаблон вопроса в черновик.
        """

        bank_item = create_bank_item_factory(
            status=BankItemStatus.ARCHIVED,
            is_active=False,
        )

        restored_item = restore_bank_item(bank_item=bank_item)

        self.assertEqual(restored_item.status, BankItemStatus.DRAFT)
        self.assertTrue(restored_item.is_active)
        self.assertIsNone(restored_item.archived_at)

    def test_publish_bank_item_rejects_item_without_options(self) -> None:
        """
        Нельзя опубликовать шаблон с вариантами без вариантов ответа.
        """

        bank_item = create_bank_item_factory()

        with self.assertRaises(ValidationError):
            publish_bank_item(bank_item=bank_item)


class QuestionBankCopyServicesTestCase(TestCase):
    """
    Тесты копирования и дублирования шаблонов.
    """

    def test_copy_bank_item_to_test_creates_question_and_options(self) -> None:
        """
        Сервис копирует шаблон вопроса в конкретный тест.
        """

        exam = create_test()
        bank_item = create_published_bank_item(
            exam=exam,
            organization=exam.organization,
            subject=exam.subject,
            owner_teacher=exam.owner_teacher,
        )

        question = copy_bank_item_to_test(
            bank_item=bank_item,
            test=exam,
        )

        self.assertIsInstance(question, QuestionModel)
        self.assertEqual(question.test, exam)
        self.assertEqual(question.source_bank_item, bank_item)
        self.assertEqual(question.text, bank_item.text)
        self.assertEqual(question.options.count(), bank_item.options.count())

    def test_copy_bank_item_to_test_rejects_draft_item(self) -> None:
        """
        Черновой шаблон нельзя скопировать в тест.
        """

        exam = create_test()
        bank_item = create_bank_item_with_options(
            exam=exam,
            organization=exam.organization,
            subject=exam.subject,
            owner_teacher=exam.owner_teacher,
        )

        with self.assertRaises(ValidationError):
            copy_bank_item_to_test(
                bank_item=bank_item,
                test=exam,
            )

    def test_duplicate_bank_item_creates_draft_copy_with_options(self) -> None:
        """
        Сервис создаёт копию шаблона вместе с вариантами.
        """

        bank_item = create_published_bank_item()

        duplicate = duplicate_bank_item(bank_item=bank_item)

        self.assertNotEqual(duplicate.id, bank_item.id)
        self.assertEqual(duplicate.status, BankItemStatus.DRAFT)
        self.assertEqual(duplicate.options.count(), bank_item.options.count())
        self.assertIn("копия", duplicate.title)
