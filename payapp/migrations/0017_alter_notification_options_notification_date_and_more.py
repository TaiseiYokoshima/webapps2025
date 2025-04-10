# Generated by Django 5.1.7 on 2025-04-09 17:59

import datetime
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("payapp", "0016_notification"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="notification",
            options={"ordering": ["-date"]},
        ),
        migrations.AddField(
            model_name="notification",
            name="date",
            field=models.DateTimeField(
                auto_now_add=True,
                default=datetime.datetime(2025, 4, 9, 17, 59, 58, 14996),
            ),
            preserve_default=False,
        ),
        migrations.AddIndex(
            model_name="notification",
            index=models.Index(fields=["date"], name="payapp_noti_date_7fcf42_idx"),
        ),
    ]
