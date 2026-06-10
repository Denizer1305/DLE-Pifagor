from __future__ import annotations


class TestStatus:
    """
    Статусы теста.
    """

    DRAFT = "draft"
    PUBLISHED = "published"
    ARCHIVED = "archived"


TEST_STATUS_CHOICES = (
    (TestStatus.DRAFT, "Черновик"),
    (TestStatus.PUBLISHED, "Опубликован"),
    (TestStatus.ARCHIVED, "Архивирован"),
)


class TestVisibility:
    """
    Видимость теста.
    """

    PRIVATE = "private"
    COURSE = "course"
    GROUPS = "groups"


TEST_VISIBILITY_CHOICES = (
    (TestVisibility.PRIVATE, "Только преподавателю"),
    (TestVisibility.COURSE, "Участникам курса"),
    (TestVisibility.GROUPS, "Назначенным группам"),
)
