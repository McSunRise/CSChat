# Generated by Django 4.2.5 on 2024-03-11 11:33

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ("chat", "0003_alter_user_uuid"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="uuid",
            field=models.UUIDField(
                default=uuid.UUID("50c72f7f-12df-4ac8-9a51-7df6cb884177"),
                editable=False,
                primary_key=True,
                serialize=False,
            ),
        ),
    ]
