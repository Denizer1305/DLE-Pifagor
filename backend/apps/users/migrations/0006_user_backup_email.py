from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("users", "0005_alter_profile_preferred_contact_method"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="backup_email",
            field=models.EmailField(
                blank=True,
                default="",
                max_length=254,
                verbose_name="Резервный email",
            ),
        ),
    ]
