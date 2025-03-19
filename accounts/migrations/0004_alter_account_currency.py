# Generated by Django 5.1.7 on 2025-03-18 20:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("accounts", "0003_account_balance"),
    ]

    operations = [
        migrations.AlterField(
            model_name="account",
            name="currency",
            field=models.CharField(
                choices=[("GBP", "GBP"), ("USD", "USD"), ("EUR", "EUR")],
                default="GBP",
                max_length=3,
            ),
        ),
    ]
