# Generated by Django 5.1.7 on 2025-04-09 23:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0006_alter_account_balance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="first_name",
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name="account",
            name="last_name",
            field=models.CharField(max_length=20),
        ),
    ]
