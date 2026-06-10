import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="DashboardItem",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "created_at",
                    models.DateTimeField(
                        auto_now_add=True, verbose_name="Дата создания"
                    ),
                ),
                (
                    "updated_at",
                    models.DateTimeField(auto_now=True, verbose_name="Дата обновления"),
                ),
                (
                    "kind",
                    models.CharField(
                        choices=[
                            ("calendar", "Событие календаря"),
                            ("note", "Заметка"),
                        ],
                        db_index=True,
                        max_length=16,
                        verbose_name="Тип",
                    ),
                ),
                ("title", models.CharField(max_length=255, verbose_name="Заголовок")),
                ("text", models.TextField(blank=True, verbose_name="Описание")),
                ("item_date", models.DateField(db_index=True, verbose_name="Дата")),
                (
                    "event_theme",
                    models.CharField(
                        choices=[
                            ("lesson", "Урок или занятие"),
                            ("checking", "Проверка работ"),
                            ("deadline", "Дедлайн"),
                            ("system", "Организационное событие"),
                            ("neutral", "Другое"),
                        ],
                        default="neutral",
                        max_length=16,
                        verbose_name="Тема события",
                    ),
                ),
                (
                    "user",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="dashboard_items",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Пользователь",
                    ),
                ),
            ],
            options={
                "verbose_name": "Элемент личного кабинета",
                "verbose_name_plural": "Элементы личного кабинета",
                "db_table": "dashboard_item",
                "ordering": ("-item_date", "-created_at"),
            },
        ),
        migrations.AddIndex(
            model_name="dashboarditem",
            index=models.Index(
                fields=["user", "kind", "item_date"],
                name="dash_item_user_kind_date_idx",
            ),
        ),
    ]
