from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("dashboard", "0001_dashboard_item"),
    ]

    operations = [
        migrations.AddField(
            model_name="dashboarditem",
            name="notification_enabled",
            field=models.BooleanField(
                default=True,
                verbose_name="Создавать уведомление",
            ),
        ),
    ]
