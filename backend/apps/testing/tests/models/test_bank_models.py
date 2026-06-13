from __future__ import annotations

from django.test import TestCase

from apps.testing.constants import (
    BankItemStatus,
    BankItemVisibility,
)
from apps.testing.models import (
    QuestionBankItem as BankItemModel,
    QuestionBankOption as BankOptionModel,
)
from apps.testing.tests.factories import (
    create_bank_item,
    create_bank_item_with_options,
    create_bank_option,
    create_published_bank_item,
)


class QuestionBankModelsTestCase(TestCase):
    """
    Smoke-тесты моделей банка тестовых заданий.
    """

    def test_create_bank_item(self) -> None:
        """
        Шаблон вопроса создаётся корректно.
        """

        bank_item = create_bank_item(
            title="Шаблон по математике",
            text="Сколько будет 2 + 2?",
        )

        self.assertIsInstance(bank_item, BankItemModel)
        self.assertEqual(bank_item.title, "Шаблон по математике")
        self.assertEqual(bank_item.text, "Сколько будет 2 + 2?")
        self.assertEqual(bank_item.status, BankItemStatus.DRAFT)
        self.assertEqual(bank_item.visibility, BankItemVisibility.PRIVATE)
        self.assertEqual(str(bank_item), "Шаблон по математике")

    def test_create_bank_option(self) -> None:
        """
        Вариант ответа шаблона создаётся корректно.
        """

        bank_item = create_bank_item()
        option = create_bank_option(
            bank_item=bank_item,
            text="4",
            is_correct=True,
            score=1,
        )

        self.assertIsInstance(option, BankOptionModel)
        self.assertEqual(option.bank_item, bank_item)
        self.assertEqual(option.text, "4")
        self.assertTrue(option.is_correct)
        self.assertEqual(str(option), "4")

    def test_create_bank_item_with_options(self) -> None:
        """
        Фабрика создаёт шаблон вопроса с двумя вариантами.
        """

        bank_item = create_bank_item_with_options()

        self.assertEqual(bank_item.options.count(), 2)
        self.assertEqual(
            bank_item.options.filter(is_correct=True).count(),
            1,
        )

    def test_create_published_bank_item(self) -> None:
        """
        Фабрика создаёт опубликованный активный шаблон.
        """

        bank_item = create_published_bank_item()

        self.assertEqual(bank_item.status, BankItemStatus.PUBLISHED)
        self.assertTrue(bank_item.is_active)
        self.assertEqual(bank_item.options.count(), 2)

    def test_bank_item_full_clean_for_valid_object(self) -> None:
        """
        Валидный шаблон вопроса проходит full_clean.
        """

        bank_item = create_bank_item()

        bank_item.full_clean()

    def test_bank_option_full_clean_for_valid_object(self) -> None:
        """
        Валидный вариант ответа шаблона проходит full_clean.
        """

        bank_item = create_bank_item()
        option = create_bank_option(
            bank_item=bank_item,
            score=1,
        )

        option.full_clean()

    def test_bank_item_str_returns_title(self) -> None:
        """
        __str__ шаблона возвращает название.
        """

        bank_item = create_bank_item(title="Контрольный вопрос")

        self.assertEqual(str(bank_item), "Контрольный вопрос")

    def test_bank_option_str_returns_short_text(self) -> None:
        """
        __str__ варианта возвращает краткий текст.
        """

        option = create_bank_option(text="Краткий вариант ответа")

        self.assertEqual(str(option), "Краткий вариант ответа")