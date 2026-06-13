from __future__ import annotations

from django.test import TestCase

from apps.testing.constants import (
    BankItemDifficulty,
    BankItemStatus,
    BankItemVisibility,
    QuestionType,
)
from apps.testing.selectors import (
    bank_item_list_queryset,
    bank_option_list_queryset,
    get_bank_item_by_id,
    get_bank_option_by_id,
    reusable_bank_item_list_queryset,
)
from apps.testing.tests.factories import (
    create_bank_item,
    create_bank_option,
    create_published_bank_item,
    create_teacher,
)


class QuestionBankItemSelectorsTestCase(TestCase):
    """
    Тесты селекторов шаблонов вопросов банка заданий.
    """

    def test_bank_item_list_queryset_filters_by_status(self) -> None:
        """
        Селектор фильтрует шаблоны по статусу.
        """

        published_item = create_published_bank_item()
        draft_item = create_bank_item(status=BankItemStatus.DRAFT)

        queryset = bank_item_list_queryset(status=BankItemStatus.PUBLISHED)

        self.assertIn(published_item, queryset)
        self.assertNotIn(draft_item, queryset)

    def test_bank_item_list_queryset_filters_by_visibility(self) -> None:
        """
        Селектор фильтрует шаблоны по видимости.
        """

        public_item = create_bank_item(visibility=BankItemVisibility.PUBLIC)
        private_item = create_bank_item(visibility=BankItemVisibility.PRIVATE)

        queryset = bank_item_list_queryset(
            visibility=BankItemVisibility.PUBLIC,
        )

        self.assertIn(public_item, queryset)
        self.assertNotIn(private_item, queryset)

    def test_bank_item_list_queryset_filters_by_difficulty(self) -> None:
        """
        Селектор фильтрует шаблоны по сложности.
        """

        easy_item = create_bank_item(difficulty=BankItemDifficulty.EASY)
        hard_item = create_bank_item(difficulty=BankItemDifficulty.HARD)

        queryset = bank_item_list_queryset(
            difficulty=BankItemDifficulty.EASY,
        )

        self.assertIn(easy_item, queryset)
        self.assertNotIn(hard_item, queryset)

    def test_bank_item_list_queryset_filters_by_question_type(self) -> None:
        """
        Селектор фильтрует шаблоны по типу вопроса.
        """

        choice_item = create_bank_item(
            question_type=QuestionType.SINGLE_CHOICE,
        )
        number_item = create_bank_item(
            question_type=QuestionType.NUMBER,
            expected_number_answer=4,
        )

        queryset = bank_item_list_queryset(
            question_type=QuestionType.SINGLE_CHOICE,
        )

        self.assertIn(choice_item, queryset)
        self.assertNotIn(number_item, queryset)

    def test_bank_item_list_queryset_filters_by_search(self) -> None:
        """
        Селектор ищет шаблоны по названию и тексту.
        """

        matched_item = create_bank_item(
            title="Теорема Пифагора",
            text="Найдите гипотенузу.",
        )
        foreign_item = create_bank_item(
            title="Закон Ома",
            text="Найдите силу тока.",
        )

        queryset = bank_item_list_queryset(search="Пифагора")

        self.assertIn(matched_item, queryset)
        self.assertNotIn(foreign_item, queryset)

    def test_get_bank_item_by_id_returns_item(self) -> None:
        """
        Селектор возвращает шаблон по идентификатору.
        """

        bank_item = create_bank_item()

        found_item = get_bank_item_by_id(bank_item.id)

        self.assertEqual(found_item, bank_item)

    def test_reusable_bank_item_list_queryset_returns_accessible_items(
        self,
    ) -> None:
        """
        Селектор возвращает доступные преподавателю шаблоны.
        """

        teacher = create_teacher()
        own_item = create_published_bank_item(
            owner_teacher=teacher,
            visibility=BankItemVisibility.PRIVATE,
        )
        public_item = create_published_bank_item(
            visibility=BankItemVisibility.PUBLIC,
        )
        foreign_private_item = create_published_bank_item(
            visibility=BankItemVisibility.PRIVATE,
        )

        queryset = reusable_bank_item_list_queryset(
            teacher_id=teacher.id,
            organization_id=own_item.organization_id,
        )

        self.assertIn(own_item, queryset)
        self.assertIn(public_item, queryset)
        self.assertNotIn(foreign_private_item, queryset)


class QuestionBankOptionSelectorsTestCase(TestCase):
    """
    Тесты селекторов вариантов шаблонов вопросов.
    """

    def test_bank_option_list_queryset_filters_by_bank_item(self) -> None:
        """
        Селектор фильтрует варианты по шаблону.
        """

        bank_item = create_bank_item()
        foreign_item = create_bank_item()

        option = create_bank_option(bank_item=bank_item)
        foreign_option = create_bank_option(bank_item=foreign_item)

        queryset = bank_option_list_queryset(bank_item_id=bank_item.id)

        self.assertIn(option, queryset)
        self.assertNotIn(foreign_option, queryset)

    def test_bank_option_list_queryset_filters_by_correct_flag(self) -> None:
        """
        Селектор фильтрует варианты по признаку правильности.
        """

        correct_option = create_bank_option(is_correct=True)
        incorrect_option = create_bank_option(is_correct=False)

        queryset = bank_option_list_queryset(is_correct=True)

        self.assertIn(correct_option, queryset)
        self.assertNotIn(incorrect_option, queryset)

    def test_get_bank_option_by_id_returns_option(self) -> None:
        """
        Селектор возвращает вариант по идентификатору.
        """

        option = create_bank_option()

        found_option = get_bank_option_by_id(option.id)

        self.assertEqual(found_option, option)