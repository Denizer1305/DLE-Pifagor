from django.apps import AppConfig


class CoreConfig(AppConfig):
    """
    Конфигурация приложения core.

    Приложение core хранит общие технические сущности проекта:
    базовые модели, исключения, permissions, pagination, responses,
    validators и вспомогательные функции.

    Это приложение не должно содержать доменную бизнес-логику.
    """

    default_auto_field = "django.db.models.BigAutoField"
    name = "core"
    verbose_name = "Ядро проекта"
